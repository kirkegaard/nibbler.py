from discord.ext import commands
import datetime
import json
import asyncio
import logging
import sys

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

description = """
Hello! Do you remember some months ago when the Earth was under attack by flying brains?
"""

extensions = [
    'extensions.rng',
    'extensions.timer',
    'extensions.member',
    'extensions.laura',
    'extensions.brain',
    'extensions.utils',
    'extensions.reddit',
    'extensions.purge'
    # 'extensions.moderator'
]

# silence discord.py
# @TODO fix this
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)

handler = logging.FileHandler(
    filename='nibbler.log', encoding='utf-8', mode='w')
logging.basicConfig(format='%(asctime)-15s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(handler)

help_attrs = dict(hidden=True)

prefix = ['!']
bot = commands.Bot(command_prefix=prefix, description=description,
                   pm_help=None, help_attrs=help_attrs)


@bot.event
async def on_ready():
    print('Ready Eddy!')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


if __name__ == '__main__':
    with open('credentials.json') as creds:
        credentials = json.load(creds)

    debug = any('debug' in arg.lower() for arg in sys.argv)
    token = credentials['token']
    bot.owner_id = credentials['owner_id']

    for extension in extensions:
        try:
            bot.load_extension(extension)
            print('Loaded extension: {}'.format(extension))
        except Exception as e:
            print('Failed to load extension {}\n{}: {}'.format(
                extension, type(e).__name__, e))

    bot.run(token)
    handlers = log.handlers[:]
    for hdlr in handlers:
        hdlr.close()
        log.removeHandler(hdlr)
