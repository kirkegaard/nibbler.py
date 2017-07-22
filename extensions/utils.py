from discord.ext import commands
import discord


class Utils():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload', hidden=True)
    async def _reload(self, extension_name: str):
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
        try:
            self.bot.load_extension(extension_name)
        except (AttributeError, ImportError) as e:
            await self.bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await self.bot.say("{} loaded.".format(extension_name))

    @commands.command()
    async def unload(self, extension_name: str):
        self.bot.unload_extension(extension_name)
        await self.bot.say("{} unloaded.".format(extension_name))


def setup(bot):
    bot.add_cog(Utils(bot))
