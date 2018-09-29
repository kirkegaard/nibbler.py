import discord
from discord.ext import commands
from utils import config
from cobe.brain import Brain
import random

brain = Brain("tmp/nibbler.brain")
REPLYS = {
    'godnat': [
        'Godnat ven :*',
        'Sov godt søtte!',
        'Drøm om mig <3'
    ],
    'godmorgen': [
        'Godmorgen hvennemand!'
    ],
    'godaften': [
        'Godaften kammerat!'
    ],
    'goddag': [
        'Hej ven <3',
        'Goddag knægt!',
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

            if random.randint(0,100) > 70:
                reply = '{} {}'.format(reply, brain.reply(reply))
            await context.channel.send(reply)

def setup(bot):
    reply = Reply(bot)
    bot.add_cog(reply)
