import requests
import spotipy
import spotipy.oauth2 as oauth2

from os import environ
from discord.ext import commands
from discord import Embed
from imdbpie import Imdb
from youtubesearchpython import SearchVideos


GOOGLE_ENDPOINT = "https://www.googleapis.com/customsearch/v1"
IMDB_ENDPOINT = "https://www.imdb.com/title/{}"


class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["g"])
    async def google(self, context, *query: str):
        """Searches google and returns the first result"""
        res = requests.get(
            GOOGLE_ENDPOINT,
            params={
                "cx": environ.get("GOOGLE_CX"),
                "key": environ.get("GOOGLE_TOKEN"),
                "q": " ".join(query),
            },
        ).json()
        res = res["items"][0]

        msg = Embed(
            colour=0x4BBFFF,
            title=res["title"],
            description=res["snippet"],
            url=res["link"],
        )

        await context.channel.send(embed=msg)

    @commands.command(aliases=["yt", "v"])
    async def youtube(self, context, *query: str):
        """Searches youtube and returns the first result"""
        search = SearchVideos(" ".join(query), offset=1, mode="dict", max_results=1)
        res = search.result()
        await context.send(res["search_result"][0]["link"])

    @commands.command()
    async def imdb(self, context, *query: str):
        """Searches imdb for a movie title"""
        imdb = Imdb()
        search = imdb.search_for_title(" ".join(query))

        imdb_id = search[0]["imdb_id"]
        res = imdb.get_title(imdb_id)
        genres = imdb.get_title_genres(imdb_id)

        rating = "Not rated"
        if "rating" in res["ratings"]:
            rating = res["ratings"]["rating"]

        title = res["base"]["title"]
        year = res["base"]["year"]
        plot_outline = res["plot"]["outline"]["text"]
        poster_url = res["base"]["image"]["url"]

        msg = Embed(
            colour=0xFFFF00,
            title="{} ({})".format(title, year),
            description="Rating: {}\nGenres: {}\nPlot: {}".format(
                rating, ", ".join(genres["genres"]), plot_outline
            ),
            url=IMDB_ENDPOINT.format(imdb_id),
        )
        msg.set_image(url=poster_url)

        await context.channel.send(embed=msg)

    @commands.command(aliases=["s"])
    async def spotify(self, context, *query: str):
        """Searches spotify for a track"""
        credentials = oauth2.SpotifyClientCredentials(
            client_id=environ.get("SPOTIFY_ID"),
            client_secret=environ.get("SPOTIFY_SECRET"),
        )

        token = credentials.get_access_token()
        sp = spotipy.Spotify(auth=token)
        res = sp.search(" ".join(query), limit=1)
        href = res["tracks"]["items"][0]["external_urls"]["spotify"]

        await context.channel.send(href)


def setup(bot):
    bot.add_cog(Search(bot))
