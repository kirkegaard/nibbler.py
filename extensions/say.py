import discord
from discord.ext import commands

from sanic import Sanic
from sanic.response import json
from sanic.response import text

class Say():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, context):
        await context.channel.send('yo')

    async def yell(self, request):
        res = request.json
        channel = self.bot.get_channel(id=res['channel_id'])
        await channel.send(res['msg'])
        return json({"success": 1})

def setup(bot):
    say = Say(bot)
    bot.add_cog(say)
    bot.api.add_route(say.yell, '/yell', methods=['POST'])