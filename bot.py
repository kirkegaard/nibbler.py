import datetime
import json
import asyncio
import logging
import sys
import discord
import traceback

from discord.ext import commands
from utils import config

from sanic import Sanic

log = logging.getLogger(__name__)

class Nibbler(commands.AutoShardedBot):
    """Nibbler"""

    def __init__(self):
        self.config = config.Config('config/bot.json')
        self.token = self.config['token']
        self.prefix = self.config['prefix']
        self.socket = self.config['socket']
        self.description = self.config['description']

        super().__init__(command_prefix=self.prefix, description=self.description,
                         pm_help=None, help_attrs=dict(hidden=True))

        if self.socket['enabled']:
            self.api = Sanic()

        for extension in self.config['extensions']:
            try:
                self.load_extension('extensions.' + extension)
                print('Loaded extension: {}'.format(extension))
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

        self.run(self.token)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)

    async def on_ready(self):
        if not hasattr(self, 'uptime'):
            self.uptime = datetime.datetime.utcnow()

        print(f'Ready: {self.user} (ID: {self.user.id})')

        if self.socket['enabled']:
            await self.api.create_server(host=self.socket['host'], port=self.socket['port'])

    async def on_resumed(self):
        print('Resumed...')

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)


nibbler = Nibbler()
