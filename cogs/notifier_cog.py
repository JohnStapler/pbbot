import os

from discord.ext.commands import Cog


class NotifierCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_user_id = int(os.getenv("AT_TARGET", 0))

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if self.target_user_id in [mention.id for mention in message.mentions]:
            target_user = await self.bot.fetch_user(self.target_user_id)
            await message.channel.send(target_user.mention)
