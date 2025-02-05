from discord.ext.commands import Cog, hybrid_command


class DevCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(description="Test if the bot is up")
    async def ping(self, ctx):
        await ctx.send("Pong!")
