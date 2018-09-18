import discord
from discord.ext import commands
from utils import config

import requests
from sanic import response


class Twitch():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')
        self.headers = {"Client-ID": self.config.get('twitch_id')}
        self.api = 'https://api.twitch.tv/helix'

    @commands.group()
    async def twitch(self, context):
        if context.invoked_subcommand is None:
            await context.send('Use `!twitch sub [user]` to subscribe to user. Or use `!twitch unsub [user]` to remove user.')

    @twitch.command()
    async def online(self, context, username):
        endpoint = '%s/streams' % self.api
        payload = {'user_login': username}
        res = requests.get(endpoint, params=payload, headers=self.headers).json()
        if not res['data']:
            return await context.send('{} is not streaming'.format(username))
        return await context.send('{} is currently streaming'.format(username))

    @twitch.command(alias=['sub'])
    async def add(self, context, username):
        endpoint = '%s/webhooks/hub' % self.api
        topic = '%s/streams' % self.api

        user_id = self.get_user_id(username)
        if not user_id:
            return False

        payload = {
            'hub.callback': '{}/callback'.format(self.config.get('bot_host')),
            'hub.mode': 'subscribe',
            'hub.topic': '{}?user_id={}'.format(topic, user_id),
        }
        res = requests.post(endpoint, params=payload, headers=self.headers)
        print(res.status_code)
        await context.send('{} added'.format(username))

    @twitch.command(alias=['unsub', 'del'])
    async def delete(self, context):
        pass

    def get_user_id(self, username):
        endpoint = '{}/users?login={}'.format(self.api, username)
        res = requests.get(endpoint, headers=self.headers).json()
        if not res['data']:
            return False
        return res['data'][0]['id']

    async def callback(self, request):
        challenge = request.args.get('hub.challenge')
        return response.html(challenge, status=200)

    async def handle(self, request):
        print(request.args)
        return response.html('', status=200)


def setup(bot):
    twitch = Twitch(bot)
    bot.add_cog(twitch)
    bot.api.add_route(twitch.callback, '/callback', methods=['GET'])
    bot.api.add_route(twitch.handle, '/callback', methods=['POST'])
