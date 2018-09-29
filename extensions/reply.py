import discord
from discord.ext import commands
from utils import config
import random

REPLYS = {
    'godnat': [
        'Godnat ven :*',
        'Sov godt søtte',
        'Drøm om mig <3'
    ],
    'godmorgen': [
        'Godmorgen hvennemand'
    ],
    'godaften': [
        'Godaften kammerat'
    ],
    'goddag': [
        'Hej ven <3',
        'Hvordan har du det?',
        'Godt at se dig søtte!',
        'Du ser godt ud i dag :D'
    ]
}


class Reply():

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, context):
        if context.author.mention == self.bot.user.mention:
            return

        first = context.content.split(' ')[0].lower()
        if first in REPLYS:
            reply = random.choice(REPLYS[first])
            await context.channel.send(reply)

def setup(bot):
    reply = Reply(bot)
    bot.add_cog(reply)
