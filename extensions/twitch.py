import discord
from discord.ext import commands
from utils import config
from sanic.response import json
from sanic.response import text
import requests


class Twitch():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')

    @commands.group()
    async def twitch(self, context):
        if context.invoked_subcommand is None:
            await context.send('Use `!twitch sub [user]` to subscribe to user. Or use `!twitch unsub [user]` to remove user.')

    @twitch.command(aliases=['sub'])
    async def sub(self, context):
        # https://api.twitch.tv/helix/webhooks/hub?hub.mode=subscribe&hub.topic=https://api.twitch.tv/helix/streams?user_id={user_id}
        pass

    @twitch.command(aliases=['unsub'])
    async def unsub(self, context):
        pass

    def get_user_id(self, username):
        pass

    async def post(self, request):
        res = request.json
        print(res)
        # if request.headers['Authorization'] == self.config.get('bot_auth'):
        #     channel = self.bot.get_channel(res['channel'])
        #     await channel.send(res['msg'])
        #     return json({"success": 1}, status=200)
        # return json({"success": 0}, status=404)


def setup(bot):
    twitch = Twitch(bot)
    bot.add_cog(twitch)
    bot.api.add_route(twitch.post, '/twitch', methods=['POST'])
