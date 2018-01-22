import discord
from discord.ext import commands

from sanic.response import json
from sanic.response import text

class Say():

    def __init__(self, bot):
        self.bot = bot

    async def sg(self, request):
        res = request.json
        if request.headers['Authorization'] == 'token hadergeorgehale':
            channel = self.bot.get_channel(res['channel'])
            await channel.send('[SG] New album from {} [{}] {}'.format(
                res['model'], res['album'], res['url'],
            ))
            return json({"success": 1}, status=200)
        return json({"success": 0}, status=404)

def setup(bot):
    say = Say(bot)
    bot.add_cog(say)
    bot.api.add_route(say.sg, '/sg', methods=['POST'])