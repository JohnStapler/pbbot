from discord.ext import commands
from discord.ext.commands import Cog


class NotifierCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="helloworld", description="View the item store")
    async def helloworld(self, ctx: commands.Context):
        await ctx.send("hello world")
