import argparse
import asyncio
import json
import os
import random
import sys
import time
from datetime import timedelta

import discord
import discord.utils
from discord.ext import commands
from dotenv import load_dotenv

from language_service import swedish_quotes
from utils import none_or_whitespace

recent_quotes = []
sync_commands = False
"""Prevent rate-limiting by only syncing commands when needed. Start with '--sync' to enable."""

# Prefix for commands
PREFIX = "/"

# JSON file to store numbers
JSON_FILE = "numbers.json"

# Initialize bot
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.hybrid_command()
async def lb(ctx):
    # Load numbers from JSON file
    numbers = load_numbers()

    # Check if there are any recorded test results
    if not numbers:
        await ctx.send("Inga testresultat finns ännu.")
        return

    # Create a list of tuples containing (WPM, user_id, quote) for each test result
    results = []
    for user_id, data in numbers.items():
        if "last_test" in data:
            wpm = data["last_test"]["number"]
            quote = data["last_test"]["quote"]
            results.append((wpm, user_id, quote))

    # Sort the results by WPM (descending order)
    results.sort(reverse=True)

    # Prepare the leaderboard message
    leaderboard_message = "**Top 10 snabbaste testresultat:**\n"
    for i, (wpm, user_id, quote) in enumerate(results[:10], start=1):
        # Get the user's display name
        user = bot.get_user(int(user_id))
        if user:
            username = user.display_name
        else:
            username = "Anonym"

        # Format WPM with one decimal place
        formatted_wpm = "{:.1f}".format(wpm)

        # Add the result to the leaderboard message
        leaderboard_message += (
            f"{i}. {username}: **{formatted_wpm} WPM** - Quote: {quote}\n"
        )

    # Send the leaderboard message
    await ctx.send(leaderboard_message)


@bot.hybrid_command()
# @commands.has_permissions(moderate_members=True)  # Kontrollera att botten har rättigheter att moderera användare
async def typing_test(ctx):
    global recent_quotes
    # Välj ett slumpmässigt citat som inte är i recent_quotes
    available_indices = [
        i for i in range(len(swedish_quotes)) if i not in recent_quotes
    ]
    if not available_indices:
        await ctx.send("Kan inte hitta fler unika citat att använda.")
        return

    quote_index = random.choice(available_indices)
    quote = swedish_quotes[quote_index]

    # Uppdatera listan med senast använda citat
    recent_quotes.append(quote_index)
    if len(recent_quotes) > 20:
        recent_quotes.pop(0)  # Ta bort det äldsta för att hålla listan till 20

    # Kontrollera om användaren har administrativa rättigheter eller en högre roll
    if (
        ctx.author.guild_permissions.administrator
        or ctx.author.top_role.position > ctx.guild.me.top_role.position
    ):
        await ctx.send("Administratörer är undantagna från timeout under nedräkningen.")
    else:
        # Timeout användaren under nedräkningen (3 sekunder)
        try:
            timeout_until = discord.utils.utcnow() + timedelta(seconds=3)
            await ctx.author.timeout(timeout_until)  # Timeout användaren i 3 sekunder
        except discord.Forbidden:
            await ctx.send(
                "Kunde inte tysta användaren. Kontrollera att boten har rätt behörigheter och att den har en högre roll än användaren."
            )
            return
        except discord.HTTPException:
            await ctx.send("Ett fel uppstod när användaren skulle tystas.")
            return

    # Skapa ett inbäddat meddelande för nedräkningen
    embed = discord.Embed(
        title="3...", description=f"**{quote}**", color=0xFF0000
    )  # Röd för 3
    countdown_message = await ctx.send(embed=embed)

    # Ändra nedräkningen till 2
    await asyncio.sleep(1)
    embed.title = "2..."
    embed.color = 0xFFA500  # Orange
    await countdown_message.edit(embed=embed)

    # Ändra nedräkningen till 1
    await asyncio.sleep(1)
    embed.title = "1..."
    embed.color = 0xFFFF00  # Gul
    await countdown_message.edit(embed=embed)

    # Ändra till "... KÖR!" och starta testet
    await asyncio.sleep(1)
    embed.title = "... KÖR!"
    embed.color = 0x00FF00  # Grön
    await countdown_message.edit(embed=embed)

    # Ta bort timeouten omedelbart när nedräkningen är över (om användaren var timeoutad)
    if not (
        ctx.author.guild_permissions.administrator
        or ctx.author.top_role.position > ctx.guild.me.top_role.position
    ):
        try:
            await ctx.author.timeout(None)
        except discord.Forbidden:
            await ctx.send(
                "Kunde inte återställa användarens skrivbehörighet. Kontrollera att boten har rätt behörigheter."
            )
            return
        except discord.HTTPException:
            await ctx.send("Ett fel uppstod när skrivbehörigheten skulle återställas.")
            return

    # Starta tidtagningen direkt när "... KÖR!" visas
    start_time = time.time()

    # Vänta på användarens inmatning efter "... KÖR!" visas
    try:
        user_input = await bot.wait_for(
            "message", check=lambda message: message.author == ctx.author, timeout=30
        )
    except asyncio.TimeoutError:
        await ctx.send("**Tiden är ute!** Försök igen.")
        return

    # Stoppa tidtagningen direkt när användaren skickar sitt meddelande
    end_time = time.time()

    # Beräkna tiden det tog att skriva
    time_taken = end_time - start_time

    # Dela upp användarens inmatning i ord och beräkna hastighet per ord
    user_words = user_input.content.split()
    quote_words = quote.split()

    # Beräkna accuracy och WPM
    correct_words = sum(a == b for a, b in zip(user_words, quote_words))
    accuracy = correct_words / len(quote_words) * 100 if quote_words else 0
    words_typed = len(user_words)
    wpm = words_typed / (time_taken / 60)

    # Skicka resultaten direkt efter att användaren trycker enter
    await ctx.send(f"Din accuracy är **{accuracy:.2f}%**.")
    await ctx.send(f"Din hastighet var **{wpm:.2f}** ord per minut.")
    await ctx.send(f"Det tog dig **{time_taken:.2f}** sekunder att skriva.")

    # Spara testresultatet om det är ett rekord
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id not in numbers:
        numbers[user_id] = {}

    if (
        "last_test" not in numbers[user_id]
        or wpm > numbers[user_id]["last_test"]["number"]
    ):
        numbers[user_id]["last_test"] = {"number": wpm, "quote": quote}
        save_numbers(numbers)
        await ctx.send("**Nytt testresultat sparades!**")
    else:
        await ctx.send(
            "Det här testresultatet var långsammare än ditt tidigare rekord och sparades inte."
        )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    if sync_commands:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} command(s)")
    else:
        print("💡 Syncing commands is disabled")
        print("   To enable syncing, start with '--sync'")


# Load numbers from JSON file
def load_numbers():
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Save numbers to JSON file
def save_numbers(numbers):
    with open(JSON_FILE, "w") as f:
        json.dump(numbers, f, indent=4)


# Command to store a number
@bot.hybrid_command()
async def nbp15(ctx, number: int):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id not in numbers:
        numbers[user_id] = {}
    if ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url
        numbers[user_id]["NPB15"] = {"number": number, "screenshot": attachment_url}
    else:
        numbers[user_id]["NPB15"] = {"number": number}
    save_numbers(numbers)
    await ctx.send(f"Nytt PB på 15S registrerat: {number} WPM")


# Command to retrieve stored number
@bot.hybrid_command()
async def pb15(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers and "NPB15" in numbers[user_id]:
        pb = numbers[user_id]["NPB15"]
        message = f'Ditt 15S PB är: {pb["number"]} WPM'
        if "screenshot" in pb:
            message += f'\nScreenshot: {pb["screenshot"]}'
        await ctx.send(message)
    else:
        await ctx.send("Inget 15S PB registrerat")


# Similarly define commands for NPB30 and PB30
@bot.hybrid_command()
async def npb30(ctx, number: int):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id not in numbers:
        numbers[user_id] = {}
    if ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url
        numbers[user_id]["NPB30"] = {"number": number, "screenshot": attachment_url}
    else:
        numbers[user_id]["NPB30"] = {"number": number}
    save_numbers(numbers)
    await ctx.send(f"Nytt PB på 30S registrerat: {number} WPM")


@bot.hybrid_command()
async def pb30(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers and "NPB30" in numbers[user_id]:
        pb = numbers[user_id]["NPB30"]
        message = f'Ditt 30S PB är: {pb["number"]} WPM'
        if "screenshot" in pb:
            message += f'\nScreenshot: {pb["screenshot"]}'
        await ctx.send(message)
    else:
        await ctx.send("Inget 30S PB registrerat")


# Command to store a number for NPB60
@bot.hybrid_command()
async def npb60(ctx, number: int):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id not in numbers:
        numbers[user_id] = {}
    if ctx.message.attachments:
        attachment_url = ctx.message.attachments[0].url
        numbers[user_id]["NPB60"] = {"number": number, "screenshot": attachment_url}
    else:
        numbers[user_id]["NPB60"] = {"number": number}
    save_numbers(numbers)
    await ctx.send(f"Nytt PB på 60S registrerat: {number} WPM")


# Command to retrieve stored number for PB60
@bot.hybrid_command()
async def pb60(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers and "NPB60" in numbers[user_id]:
        pb = numbers[user_id]["NPB60"]
        message = f'Ditt 60S PB är: {pb["number"]} WPM'
        if "screenshot" in pb:
            message += f'\nScreenshot: {pb["screenshot"]}'
        await ctx.send(message)
    else:
        await ctx.send("Inget 60S PB registrerat")


# Command to show all stored PBs for a user
@bot.hybrid_command()
async def pb(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers:
        message = "Här är dina PB:s\n"
        if "NPB15" in numbers[user_id]:
            pb = numbers[user_id]["NPB15"]
            if isinstance(pb, int):
                message += f"15S = {pb} WPM\n"
            else:
                message += f"15S = {pb['number']} WPM\n"
        else:
            message += "15S = Inget registrerat\n"
        if "NPB30" in numbers[user_id]:
            pb = numbers[user_id]["NPB30"]
            if isinstance(pb, int):
                message += f"30S = {pb} WPM\n"
            else:
                message += f"30S = {pb['number']} WPM\n"
        else:
            message += "30S = Inget registrerat\n"
        if "NPB60" in numbers[user_id]:
            pb = numbers[user_id]["NPB60"]
            if isinstance(pb, int):
                message += f"60S = {pb} WPM"
            else:
                message += f"60S = {pb['number']} WPM"
        else:
            message += "60S = Inget registrerat"
        await ctx.send(message)
    else:
        await ctx.send("Inga PB registrerade för dig")


# Command to show all available commands
@bot.hybrid_command()
async def jelp(ctx):
    commands_list = [
        "**/NPB15** - Registrerar ett nytt PB på 15S.",
        "**/PB15** - Visar ditt registrerade PB på 15S.",
        "**/NPB30** - Registrerar ett nytt PB på 30S.",
        "**/PB30** - Visar ditt registrerade PB på 30S.",
        "**/NPB60** - Registrerar ett nytt PB på 60S.",
        "**/PB60** - Visar ditt registrerade PB på 60S.",
        "**/PB** - Visar alla dina registrerade PB.",
        "**/3MR** - Förklarar vad treminutersregeln är.",
        "**/test** - Skriv ett hastighetstest så snabbt du bara kan!",
        "**/LB** - Visar top 10 snabbast skrivna quotes från /test",
    ]
    help_message = "Här är en lista över tillgängliga kommandon:\n\n"
    help_message += "\n".join(commands_list)
    await ctx.send(help_message)


@bot.hybrid_command()
async def tmr(ctx):
    text = "#3MR är kort för **treminutersregeln**. Det är regeln man kan tillämpa när man skriver hastighetstest för att få goda resultat oftare. Den går ut på att man tar en paus på tre minuter mellan varje test. Detta gör man för att återställa sinnestämningen men också för att få tillbaka energin."
    await ctx.send(text)


def parse_arguments() -> dict:
    parser = argparse.ArgumentParser(prog="PB Bot")
    parser.add_argument("--sync", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv(override=True)
    TOKEN = os.getenv("DISCORD_TOKEN")

    arguments = parse_arguments()
    sync_commands = arguments.sync

    if none_or_whitespace(TOKEN):
        print("Please set the 'DISCORD_TOKEN' environment variable.\n")
        sys.exit(1)

    bot.run(TOKEN)
