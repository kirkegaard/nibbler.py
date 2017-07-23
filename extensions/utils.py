import discord
import datetime
import logging
from discord.ext import commands

log = logging.getLogger(__name__)
client = discord.Client()


class Utils():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, context):
        """Pings the bot"""
        msg = await context.channel.send('Pong!!!')
        lag = msg.created_at - context.message.created_at
        await msg.edit(content='Pong!!! ({}ms)'.format(lag.microseconds / 100))

    @commands.command(name='reload')
    async def _reload(self, context, extension_name: str):
        """Reload an extension"""
        try:
            self.bot.unload_extension('extensions.' + extension_name)
            self.bot.load_extension('extensions.' + extension_name)
        except Exception as e:
            await context.send('\N{PISTOL}')
            await context.send('{}: {}'.format(type(e).__name__, e))
        else:
            await context.send('\N{OK HAND SIGN}')

    @commands.command()
    async def load(self, context, extension_name: str):
        """Loads an extension"""
        try:
            self.bot.load_extension('extensions.' + extension_name)
        except (AttributeError, ImportError) as e:
            await context.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await context.send("{} loaded.".format(extension_name))

    @commands.command()
    async def unload(self, context, extension_name: str):
        """Unloads an extension"""
        self.bot.unload_extension('extensions.' + extension_name)
        await context.send("{} unloaded.".format(extension_name))

    @commands.command()
    async def purge(self, context):
        """Clean up the channel history"""
        await context.message.delete()
        last_week = datetime.datetime.now() - datetime.timedelta(days=7)
        async for msg in context.message.channel.history(limit=10000000000000, before=last_week):
            if msg.pinned:
                continue

            stringTime = msg.created_at.strftime("%Y-%m-%d %H:%M")
            try:
                author = msg.author
            except:
                author = 'invalid'

            message = str(msg.content)
            template = '[Purge][{stringTime}] <{author}> {message}\n'

            await msg.delete()
            print(template.format(stringTime=stringTime,
                                  author=author, message=message)[:-1])


def setup(bot):
    bot.add_cog(Utils(bot))
