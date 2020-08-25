import requests
import requests_cache
from discord.ext import commands
from random import randint


class Dadjoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, context):
        """Tells a dad joke"""
        headers = {"Accept": "text/plain"}
        with requests_cache.disabled():
            res = requests.get("https://icanhazdadjoke.com", headers=headers)
        await context.send(res.text)


def setup(bot):
    bot.add_cog(Dadjoke(bot))
