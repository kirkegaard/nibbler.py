import discord
import datetime
import logging
from discord.ext import commands

log = logging.getLogger(__name__)


class Utils():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload')
    async def _reload(self, extension_name: str):
        """Reload an extension"""
        try:
            self.bot.unload_extension(extension_name)
            self.bot.load_extension(extension_name)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command()
    async def load(self, extension_name: str):
        """Loads an extension"""
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} loaded.".format(extension_name))

    @commands.command()
    async def unload(self, extension_name: str):
        """Unloads an extension"""
        self.bot.unload_extension(extension_name)
        await self.bot.say("{} unloaded.".format(extension_name))

    @commands.command(pass_context=True)
    async def purge(self, context):
        """Clean up the channel history"""
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

            log.info(template.format(stringTime=stringTime,
                                     author=author, message=message)[:-1])


def setup(bot):
    bot.add_cog(Utils(bot))
