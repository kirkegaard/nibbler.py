import discord
from discord.ext import commands
from utils import config

from sanic.response import json
from sanic.response import text


class Speak():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')

    async def say(self, request):
        res = request.json
        if request.headers['Authorization'] == self.config.get('bot_auth'):
            channel = self.bot.get_channel(res['channel'])
            await channel.send(res['msg'])
            return json({"success": 1}, status=200)
        return json({"success": 0}, status=404)

    async def sg(self, request):
        res = request.json
        if request.headers['Authorization'] == self.config.get('bot_auth'):
            channel = self.bot.get_channel(res['channel'])
            await channel.send('[SG] New album from {} [{}] {}'.format(
                res['model'], res['album'], res['url'],
            ))
            return json({"success": 1}, status=200)
        return json({"success": 0}, status=404)


def setup(bot):
    speak = Speak(bot)
    bot.add_cog(speak)
    bot.api.add_route(speak.say, '/say', methods=['POST'])
    bot.api.add_route(speak.sg, '/sg', methods=['POST'])
