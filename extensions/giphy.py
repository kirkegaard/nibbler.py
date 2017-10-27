import requests
import requests_cache
from utils import config
from discord.ext import commands


class Giphy():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')
        self.apikey = self.config.get('giphy_token')

    @commands.command(aliases=['gif'])
    async def search(self, context, *query: str):
        """ Search for a gif on giphy"""
        endpoint = '/v1/gifs/random'
        params = {
            'api_key': self.apikey,
            'tag': query
        }

        with requests_cache.disabled():
            res = requests.get('http://api.giphy.com%s' % endpoint, params=params).json()

        await context.send(res['data']['url'])


def setup(bot):
    bot.add_cog(Giphy(bot))
