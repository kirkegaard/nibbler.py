import re
import discord
import requests
import google
from discord.ext import commands
from imdbpie import Imdb


class Search():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g'])
    async def google(self, context, *query: str):
        """Searches google and returns the first result"""
        result = google.search(' '.join(query), num=1,
                               user_agent=google.get_random_user_agent())
        await context.channel.send(next(result))

    @commands.command(aliases=['yt', 'v'])
    async def video(self, context, *query: str):
        """Searches google video (youtube) and returns the first result"""
        result = google.search(
            ' '.join(query), num=1, user_agent=google.get_random_user_agent(), tpe='vid')
        await context.channel.send(next(result))

    @commands.command(aliases=['c', 'calc'])
    async def valuta(self, context, *query: str):
        """Converts a valuta through google finance"""
        v = float(query[0])
        f = query[1].upper()
        t = query[3].upper()

        endpoint = "https://api.fixer.io/latest?symbols={},{}".format(f, t)
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
            url='https://www.imdb.com/title/{}'.format(res.imdb_id)
        )
        msg.set_image(url=res.poster_url)

        await context.channel.send(embed=msg)


def setup(bot):
    bot.add_cog(Search(bot))
