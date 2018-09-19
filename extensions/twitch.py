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
        #self.channel = 482186488340283402
        self.channel = 483727348596998144

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
            'hub.lease_seconds': 864000,
            'hub.topic': '{}?user_id={}'.format(topic, user_id),
        }
        res = requests.post(endpoint, params=payload, headers=self.headers)
        print(res.status_code)
        await context.send('{} added'.format(username))

    @twitch.command(alias=['unsub', 'del'])
    async def delete(self, context):
        pass

    def get_user(self, user_id):
        endpoint = '{}/users?id={}'.format(self.api, user_id)
        res = requests.get(endpoint, headers=self.headers).json()
        if not res['data']:
            return False
        return res['data'][0]

    def get_user_id(self, username):
        endpoint = '{}/users?login={}'.format(self.api, username)
        res = requests.get(endpoint, headers=self.headers).json()
        if not res['data']:
            return False
        return res['data'][0]['id']

    async def callback(self, request):
        challenge = request.args.get('hub.challenge')
        return response.text(challenge, status=200)

    async def handle(self, request):
        data = request.json['data']
        if not data:
            return False
        user_id = data[0]['user_id']
        channel = self.bot.get_channel(self.channel)
        user = self.get_user(user_id)
        await channel.send('{u[display_name]} is streaming at https://twitch.tv/{u[login]}'.format(u=user))
        return response.text('', status=200)


def setup(bot):
    twitch = Twitch(bot)
    bot.add_cog(twitch)
    bot.api.add_route(twitch.callback, '/callback', methods=['GET'])
    bot.api.add_route(twitch.handle, '/callback', methods=['POST'])
