import discord
from discord.ext import commands
import json
import random
import time
import asyncio
from datetime import timedelta, datetime
import discord.utils
import os

# Bot token
TOKEN = os.getenv("DISCORD_TOKEN")

recent_quotes = []

# List of random Swedish quotes
swedish_quotes = [
    "Lycka är inte något du hittar, det är något du skapar.",
    "Det är aldrig för sent att ge upp det du är, för att bli det du kan bli.",
    "Ju hårdare du arbetar, desto mer tur får du.",
    "Ge aldrig upp, för det är just när allting verkar hopplöst som chansen dyker upp.",
    "Det är bättre att försöka och misslyckas än att aldrig försöka alls.",
    "Förändring är svårt i början, rörig i mitten, men vacker i slutet.",
    "Du är starkare än du tror, modigare än du verkar, och smartare än du tror.",
    "Varje dag är en ny början, ta en djup andetag och börja igen.",
    "För att lyckas måste du tro att du kan.",
    "Att följa sina drömmar är ett modigt val, men det är vägen till verklig lycka.",
    "Det är våra val som visar vad vi verkligen är, mycket mer än våra förmågor.",
    "Tiden läker inte alla sår, men den lär oss att leva med dem.",
    "Livet är en resa och bara du kan bestämma riktningen.",
    "Tillåt inte din rädsla att styra ditt liv, låt ditt mod leda dig istället.",
    "Det är aldrig för sent att börja om och skapa det liv du önskar.",
    "Ibland måste du gå igenom det värsta för att nå det bästa.",
    "Varje hinder är en möjlighet att växa och lära sig.",
    "För att förändra ditt liv måste du först förändra dina tankar.",
    "För att uppnå stora saker måste du våga ta stora risker.",
    "Livet är för kort för att spendera det på att ångra sig, så lev utan ånger.",
    "Det är aldrig för sent att bli den person du alltid velat vara.",
    "Varje dag är en gåva, använd den klokt och gör det bästa av den.",
    "Det är dina handlingar, inte dina ord, som definierar dig som person.",
    "För att bli framgångsrik måste du tro på dig själv när ingen annan gör det.",
    "Tillåt dig själv att växa och blomstra, även om det innebär att du måste kämpa.",
    "Förändring är smärtsam, men ingenting är så smärtsamt som att stanna kvar där du inte hör hemma.",
    "Ge aldrig upp på dina drömmar, även när det känns som om hela världen är emot dig.",
    "Att leva ett liv utan ånger kräver mod, men det är värt det i slutändan.",
    "Tiden går oavsett om du gör något med den eller inte, så varje dag är en möjlighet att göra det bästa av det.",
    "För att växa måste du lämna din komfortzon och ta itu med det okända.",
    "Ditt öde ligger i dina händer, så ta kontroll över det och forma det till det liv du önskar.",
    "Livet är för kort för att spendera det på att vara olycklig, så gör det som gör dig lycklig.",
    "Att leva i nuet är den bästa gåva du kan ge dig själv, så släpp taget om det förflutna och se framåt.",
    "Varje dag är en ny början, så släpp taget om det förflutna och fokusera på framtiden.",
    "Att våga drömma stort är det första steget mot att uppnå stora saker.",
    "Ingenting i livet är en garanti, så varje dag är en gåva att uppskatta och njuta av.",
    "Det är genom att följa ditt hjärta som du hittar verklig lycka och mening i livet.",
    "Att leva ett liv utan ånger kräver mod, men det är också det mest givande.",
    "Varje dag är en möjlighet att förändra ditt liv, så ta chansen och skapa det liv du önskar.",
    "Att våga drömma stort är det första steget mot att uppnå stora saker.",
    "Det är dina handlingar, inte dina ord, som definierar dig som person.",
    "Ingenting kan hindra dig om du har modet att fortsätta framåt trots motgångar.",
    "Att våga tro på dig själv är det första steget mot att uppnå dina drömmar.",
    "Livet är en resa och bara du kan bestämma riktningen.",
    "Det är bättre att ångra det du gjorde än att ångra det du inte gjorde.",
    "Ingenting är omöjligt för den som tror att allt är möjligt.",
    "Att följa dina drömmar kräver mod, men det är det som leder till verklig lycka och framgång.",
    "Varje dag är en gåva, så var tacksam för det du har och uppskatta varje ögonblick.",
    "Det är genom att följa ditt hjärta som du hittar verklig lycka och mening i livet.",
    "Att våga tro på dig själv är det första steget mot att uppnå dina drömmar.",
    "Ingenting i livet är en garanti, så varje dag är en gåva att uppskatta och njuta av.",
    "Förändring är oundviklig, så omfamna den och låt den leda dig mot nya möjligheter.",
    "Att leva i nuet är det bästa sättet att uppskatta livet och allt det har att erbjuda.",
    "Varje dag är en ny början, så släpp taget om det förflutna och fokusera på framtiden.",
    "Att våga drömma stort är det första steget mot att uppnå stora saker.",
    "Ingenting i livet är en garanti, så varje dag är en gåva att uppskatta och njuta av.",
    "Det är genom att följa ditt hjärta som du hittar verklig lycka och mening i livet.",
    "Att leva ett liv utan ånger kräver mod, men det är också det mest givande.",
    "Varje dag är en möjlighet att förändra ditt liv, så ta chansen och skapa det liv du önskar.",
    "Att våga drömma stort är det första steget mot att uppnå stora saker.",
    "Det är dina handlingar, inte dina ord, som definierar dig som person.",
    "Ingenting kan hindra dig om du har modet att fortsätta framåt trots motgångar.",
    "Att våga tro på dig själv är det första steget mot att uppnå dina drömmar.",
    "Livet är en resa och bara du kan bestämma riktningen.",
    "Det är bättre att ångra det du gjorde än att ångra det du inte gjorde.",
    "Ingenting är omöjligt för den som tror att allt är möjligt.",
    "Att följa dina drömmar kräver mod, men det är det som leder till verklig lycka och framgång.",
    "Varje dag är en gåva, så var tacksam för det du har och uppskatta varje ögonblick.",
    "Det är genom att följa ditt hjärta som du hittar verklig lycka och mening i livet.",
    "Att våga tro på dig själv är det första steget mot att uppnå dina drömmar.",
    "Ingenting i livet är en garanti, så varje dag är en gåva att uppskatta och njuta av.",
    "Förändring är oundviklig, så omfamna den och låt den leda dig mot nya möjligheter.",
    "Att leva i nuet är det bästa sättet att uppskatta livet och allt det har att erbjuda.",
    "Varje dag är en ny början, så släpp taget om det förflutna och fokusera på framtiden.",
    "Att våga drömma stort är det första steget mot att uppnå stora saker.",
    "Ingenting i livet är en garanti, så varje dag är en gåva att uppskatta och njuta av.",
    "Det är genom att följa ditt hjärta som du hittar verklig lycka och mening i livet.",
    "Att leva ett liv utan ånger kräver mod, men det är också det mest givande.",
    "Varje dag är en möjlighet att förändra ditt liv, så ta chansen och skapa det liv du önskar.",
    "Att våga drömma stort är det första steget mot att uppnå stora saker.",
    "Det är dina handlingar, inte dina ord, som definierar dig som person.",
    "Ingenting kan hindra dig om du har modet att fortsätta framåt trots motgångar.",
    "Att våga tro på dig själv är det första steget mot att uppnå dina drömmar.",
    "Livet är en resa och bara du kan bestämma riktningen.",
    "Det är bättre att ångra det du gjorde än att ångra det du inte gjorde.",
    "Ingenting är omöjligt för den som tror att allt är möjligt.",
    "Att följa dina drömmar kräver mod, men det är det som leder till verklig lycka och framgång.",
    "Varje dag är en gåva, så var tacksam för det du har och uppskatta varje ögonblick.",
]

# Prefix for commands
PREFIX = "/"

# JSON file to store numbers
JSON_FILE = "numbers.json"

# Initialize bot
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.command()
async def LB(ctx):
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


@bot.command(aliases=["test"])
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
@bot.command(aliases=["npb15"])
async def NPB15(ctx, number: int):
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
@bot.command(aliases=["pb15"])
async def PB15(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers and "NPB15" in numbers[user_id]:
        pb = numbers[user_id]["NPB15"]
        message = f'Ditt 15S PB är: {pb["number"]} WPM'
        if "screenshot" in pb:
            message += f'\nScreenshot: {pb["screenshot"]}'
        await ctx.send(message)
    else:
        await ctx.send(f"Inget 15S PB registrerat")


# Similarly define commands for NPB30 and PB30
@bot.command(aliases=["npb30"])
async def NPB30(ctx, number: int):
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


@bot.command(aliases=["pb30"])
async def PB30(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers and "NPB30" in numbers[user_id]:
        pb = numbers[user_id]["NPB30"]
        message = f'Ditt 30S PB är: {pb["number"]} WPM'
        if "screenshot" in pb:
            message += f'\nScreenshot: {pb["screenshot"]}'
        await ctx.send(message)
    else:
        await ctx.send(f"Inget 30S PB registrerat")


# Command to store a number for NPB60
@bot.command(aliases=["npb60"])
async def NPB60(ctx, number: int):
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
@bot.command(aliases=["pb60"])
async def PB60(ctx):
    user_id = str(ctx.author.id)
    numbers = load_numbers()
    if user_id in numbers and "NPB60" in numbers[user_id]:
        pb = numbers[user_id]["NPB60"]
        message = f'Ditt 60S PB är: {pb["number"]} WPM'
        if "screenshot" in pb:
            message += f'\nScreenshot: {pb["screenshot"]}'
        await ctx.send(message)
    else:
        await ctx.send(f"Inget 60S PB registrerat")


# Command to show all stored PBs for a user
@bot.command(aliases=["pb"])
async def PB(ctx):
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
        await ctx.send(f"Inga PB registrerade för dig")


# Command to show all available commands
@bot.command(aliases=["Help"])
async def Jelp(ctx):
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


@bot.command(aliases=["3MR", "3mr"])
async def TMR(ctx):
    text = "#3MR är kort för **treminutersregeln**. Det är regeln man kan tillämpa när man skriver hastighetstest för att få goda resultat oftare. Den går ut på att man tar en paus på tre minuter mellan varje test. Detta gör man för att återställa sinnestämningen men också för att få tillbaka energin."
    await ctx.send(text)


# Run the bot
bot.run(TOKEN)
