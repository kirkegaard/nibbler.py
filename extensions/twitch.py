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
        self.callback = '{}/callback'.format(self.config.get('bot_host'))
        self.headers = {"Client-ID": self.config.get('twitch_id')}

    @commands.group()
    async def twitch(self, context):
        if context.invoked_subcommand is None:
            await context.send('Use `!twitch sub [user]` to subscribe to user. Or use `!twitch unsub [user]` to remove user.')

    @twitch.command(alias=['sub'])
    async def add(self, context, username):
        endpoint = 'https://api.twitch.tv/helix/webhooks/hub'
        topic = 'https://api.twitch.tv/helix/streams'

        user_id = self.get_user_id(username)
        if not user_id:
            return False

        payload = {
            'hub.callback': self.callback,
            'hub.mode': 'subscribe',
            'hub.topic': '{}?user_id={}'.format(topic, user_id),
        }
        res = requests.post(endpoint, params=payload, headers=self.headers)
        print(self.callback, user_id, payload, res)

    @twitch.command(alias=['unsub', 'del'])
    async def delete(self, context):
        pass

    def get_user_id(self, username):
        endpoint = 'https://api.twitch.tv/helix/users?login={}'.format(username)
        res = requests.get(endpoint, headers=self.headers).json()
        if not res['data']:
            return False
        return res['data'][0]['id']

    async def callback(self, request):
        print(request)
        return json({}, status=200)
        # if request.headers['Authorization'] == self.config.get('bot_auth'):
        #     channel = self.bot.get_channel(res['channel'])
        #     await channel.send(res['msg'])
        #     return json({"success": 1}, status=200)
        # return json({"success": 0}, status=404)


def setup(bot):
    twitch = Twitch(bot)
    bot.add_cog(twitch)
    bot.api.add_route(twitch.callback, '/callback', methods=['GET'])
