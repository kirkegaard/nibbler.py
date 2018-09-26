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

    @twitch.command()
    async def sub(self, context, username):
        endpoint = '%s/webhooks/hub' % self.api
        topic = '%s/streams' % self.api

        user_id = self.get_user_id(username)
        if not user_id:
            return False

        channel = '{}/callback?channel={}'.format(self.config.get('bot_host'), context.channel.id)
        payload = {
            'hub.callback': channel,
            'hub.mode': 'subscribe',
            'hub.lease_seconds': 864000,
            'hub.topic': '{}?user_id={}'.format(topic, user_id),
        }

        res = requests.post(endpoint, params=payload, headers=self.headers)
        if res.status_code == 202:
            await context.send('{} added'.format(username))

    @twitch.command()
    async def list(self, context):
        subscriptions = self.get_subscriptions()
        if not subscriptions:
            return False

        for k, v in enumerate(subscriptions['data']):
            topic = self.parse_url(v['topic'])
            user = self.get_user(topic['user_id'])
            username = user['display_name']

            callback = self.parse_url(v['callback'])
            channel = callback['channel']

            await context.send('[{}] {} : {}'.format(k, username, channel))

    @twitch.command()
    async def unsub(self, context, idx: int):
        endpoint = '%s/webhooks/hub' % self.api
        subscriptions = self.get_subscriptions()
        if not subscriptions:
            return False

        subscription = subscriptions['data'][idx]
        payload = {
            'hub.mode': 'unsubscribe',
            'hub.callback': subscription['callback'],
            'hub.topic': subscription['topic']
        }
        res = requests.post(endpoint, params=payload, headers=self.headers)
        if res.status_code == 202:
            await context.send('Subscription removed')

    def get_subscriptions(self):
        endpoint = '%s/webhooks/subscriptions' % self.api
        access_token = self.get_access_token()
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        res = requests.get(endpoint, headers=headers).json()
        return res

    def parse_url(self, url):
        query = requests.utils.urlparse(url).query
        params = dict(x.split('=') for x in query.split('&'))
        return params

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

    def get_access_token(self):
        endpoint = 'https://id.twitch.tv/oauth2/token'
        payload = {
            'client_id': self.config.get('twitch_id'),
            'client_secret': self.config.get('twitch_secret'),
            'grant_type': 'client_credentials'
        }
        res = requests.post(endpoint, params=payload).json()
        return res['access_token']

    async def callback(self, request):
        challenge = request.args.get('hub.challenge')
        return response.text(challenge, status=200)

    async def handle(self, request):
        data = request.json.get('data')
        if not data:
            return response.text('', status=200)

        user_id = data[0]['user_id']
        user = self.get_user(user_id)

        channel_id = int(request.args.get('channel'))
        channel = self.bot.get_channel(channel_id)

        await channel.send('{display_name} is streaming at https://twitch.tv/{login}'.format(
            display_name=user['display_name'],
            login=user['login']
        ))
        return response.text('', status=200)


def setup(bot):
    twitch = Twitch(bot)
    bot.add_cog(twitch)
    bot.api.add_route(twitch.callback, '/callback', methods=['GET'])
    bot.api.add_route(twitch.handle, '/callback', methods=['POST'])
