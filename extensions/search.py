import discord
import requests
import google
from discord.ext import commands


class Search():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g'])
    async def google(self, context, *query: str):
        """Searches google and returns the first result"""
        result = google.lucky(' '.join(query))
        await context.channel.send(result)

    @commands.command(aliases=['yt', 'v'])
    async def video(self, context, *query: str):
        """Searches google video (youtube) and returns the first result"""
        result = google.search_videos(' '.join(query), num=1)
        await context.channel.send(next(result))


def setup(bot):
    bot.add_cog(Search(bot))
