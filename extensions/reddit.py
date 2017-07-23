import discord
import logging
import random
import requests
import json

from discord.ext import commands

SUBREDDITS_PORN = [
    'nsfw',
    'Amateur',
    'Blowjobs',
    'GirlsFinishingTheJob',
    'NSFW_GIF',
    'creampies',
    'cumsluts',
    'dirtysmall',
    'facesitting',
    'nsfw_gifs',
    'nsfwhardcore',
    'omgbeckylookathiscock',
    'porn_gifs'
]

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}


class Reddit():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def porn(self, context):
        """Fetches a random picture from subreddits. *NSFW channels only"""
        if not context.message.channel.is_nsfw():
            await context.send("This isnt a nsfw channel")
            return

        endpoint = 'http://reddit.com/r/{}/random/.json'.format(
            random.choice(SUBREDDITS_PORN))
        data = requests.get(endpoint, headers=headers).json()
        msg = data[0]["data"]["children"][0]["data"]["url"]
        await context.send(msg)


def setup(bot):
    bot.add_cog(Reddit(bot))
