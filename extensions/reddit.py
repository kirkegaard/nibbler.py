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
];

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

class Reddit():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def porn(self, context):
        if 'nsfw' not in context.message.channel.name:
            await self.bot.say("This isnt a nsfw channel")
            return

        endpoint = 'http://reddit.com/r/{}/random/.json'.format(random.choice(SUBREDDITS_PORN));
        data = requests.get(endpoint, headers=headers).json()
        msg = data[0]["data"]["children"][0]["data"]["url"]
        await self.bot.say(msg)

def setup(bot):
    bot.add_cog(Reddit(bot))