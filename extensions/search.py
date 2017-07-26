import re
import discord
import requests
import json
import spotipy
import spotipy.oauth2 as oauth2

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
        self.settings = {
            'google': {
                'endpoint': 'https://www.googleapis.com/customsearch/v1',
                'cx': self.config.get('google_cx'),
                'key': self.config.get('google_token')
            },
            'spotify': {
                'client_id': self.config.get('spotify_id'),
                'client_secret': self.config.get('spotify_secret')
            },
            'imdb': {
                'endpoint': 'https://www.imdb.com/title/{}'
            },
            'fixer': {
                'endpoint': "http://api.fixer.io/latest?base={}"
            }
        }

    @commands.command(aliases=['s'])
    async def spotify(self, context, *query: str):
        """Searches spotify for a track"""
        credentials = oauth2.SpotifyClientCredentials(
            client_id=self.settings['spotify']['client_id'],
            client_secret=self.settings['spotify']['client_secret'])

        token = credentials.get_access_token()
        sp = spotipy.Spotify(auth=token)
        res = sp.search(' '.join(query), limit=1)
        href = res['tracks']['items'][0]['external_urls']['spotify']

        await context.channel.send(href)

    @commands.command(aliases=['g'])
    async def google(self, context, *query: str):
        """Searches google and returns the first result"""
        self.settings['google']['q'] = ' '.join(query)
        res = requests.get(
            self.settings['google']['endpoint'], params=self.settings['google']).json()
        res = res['items'][0]

        msg = discord.Embed(
            colour=0x4BBFFF,
            title=res['title'],
            description=res['snippet'],
            url=res['link']
        )

        await context.channel.send(embed=msg)

    @commands.command(aliases=['yt', 'v'])
    async def youtube(self, context, *query: str):
        """Searches youtube and returns the first result"""
        yt = build('youtube', 'v3',
                   developerKey=self.settings['google']['key'])
        query = yt.search().list(q=' '.join(
            query), part="id, snippet", maxResults=1).execute()
        res = query.get('items', [])

        videoId = res[0]['id']['videoId']

        await context.channel.send(f'https://www.youtube.com/watch?v={videoId}')

    @commands.command(aliases=['c', 'calc'])
    async def valuta(self, context, *query: str):
        """Converts a valuta through google finance"""
        v = float(query[0])
        f = query[1].upper()
        t = query[3].upper()

        endpoint = self.settings['fixer']['endpoint'].format(f)
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
            url=self.settings['imdb']['endpoint'].format(res.imdb_id)
        )
        msg.set_image(url=res.poster_url)

        await context.channel.send(embed=msg)


def setup(bot):
    bot.add_cog(Search(bot))
