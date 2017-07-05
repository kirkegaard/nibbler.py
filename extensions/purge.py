import datetime
import discord
from discord.ext import commands
import logging

log = logging.getLogger(__name__)

class purge():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def purge(self, context):
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        async for msg in self.bot.logs_from(context.message.channel, limit=10000000000000, before=last_week):
            if msg.pinned:
                continue

            stringTime = msg.timestamp.strftime("%Y-%m-%d %H:%M")
            try:
                author = msg.author
            except:
                author = 'invalid'

            message = str(msg.content)
            template = '[Purge][{stringTime}] <{author}> {message}\n'

            await self.bot.delete_message(msg)

            log.info(template.format(stringTime=stringTime, author=author, message=message)[:-1])


def setup(bot):
    bot.add_cog(purge(bot))