from random import randint
import requests
import requests_cache
from discord.ext import commands


class Dadjoke():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dadjoke(self, context):
        """Tells a dad joke"""
        headers = {"Accept": "text/plain"}
        with requests_cache.disabled():
            res = requests.get('https://icanhazdadjoke.com', headers=headers)
        await context.send(res.text)

    async def on_message(self, message):
        if message.content.lower().startswith('jeg er'):
            rand = randint(0, 1000)
            if rand == 69:
                msg = message.content.lower().replace('jeg er', 'Hej, ')
                await message.channel.send('%s. Jeg er far.' % msg)


def setup(bot):
    bot.add_cog(Dadjoke(bot))
