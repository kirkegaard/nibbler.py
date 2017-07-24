import re
import discord
import requests
import json

from utils import config
from discord.ext import commands
from imdbpie import Imdb

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


class Search():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')
        self.endpoint = {
            'google': 'https://www.googleapis.com/customsearch/v1',
            'imdb': 'https://www.imdb.com/title/{}'
        }
        self.params_google = {
            'key': self.config.get('google_token'),
            'cx': self.config.get('google_cx')
        }

    @commands.command(aliases=['g'])
    async def google(self, context, *query: str):
        """Searches google and returns the first result"""
        self.params_google['q'] = ' '.join(query)
        res = requests.get(
            self.endpoint['google'], params=self.params_google).json()
        res = res['items'][0]

        msg = discord.Embed(
            colour=0x4BBFFF,
            title=res['title'],
            description=res['snippet'],
            url=res['link']
        )

        await context.channel.send(embed=msg)

    @commands.command(aliases=['yt', 'v'])
    async def video(self, context, *query: str):
        """Searches google video (youtube) and returns the first result"""
        youtube = build('youtube', 'v3',
                        developerKey=self.params_google['key'])
        query = youtube.search().list(q=' '.join(
            query), part="snippet", maxResults=1).execute()
        res = query.get('items', [])

        videoId = res[0]['id']['videoId']
        res = res[0]['snippet']

        msg = discord.Embed(
            colour=0xDF080E,
            title=res['title'],
            description=res['description'],
            url='https://www.youtube.com/watch?v={}'.format(videoId)
        )
        msg.set_image(url=res['thumbnails']['high']['url'])

        await context.channel.send(embed=msg)

    @commands.command(aliases=['c', 'calc'])
    async def valuta(self, context, *query: str):
        """Converts a valuta through google finance"""
        v = float(query[0])
        f = query[1].upper()
        t = query[3].upper()

        endpoint = "http://api.fixer.io/latest?base={}".format(f)
        res = requests.get(endpoint).json()

        await context.send('Result: {} {}'.format(v * res['rates'][t], t))

    @commands.command()
    async def imdb(self, context, *query: str):
        """Searches imdb for a movie title"""
        imdb = Imdb(anonymize=True)
        search = imdb.search_for_title(query)
        res = imdb.get_title_by_id(search[0]['imdb_id'])

        msg = discord.Embed(
            colour=0xffff00,
            title='{} ({})'.format(res.title, res.year),
            description='Rating: {}\nGenres: {}\nPlot: {}'.format(
                res.rating, ', '.join(res.genres), res.plot_outline),
            url=self.endpoint['imdb'].format(res.imdb_id)
        )
        msg.set_image(url=res.poster_url)

        await context.channel.send(embed=msg)


def setup(bot):
    bot.add_cog(Search(bot))
