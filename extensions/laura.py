from random import randint
from discord.ext import commands

class Laura():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        rand = randint(0, 1000)
        msg = None

        if rand == 69:
            msg = 'Laura er sød <3'

        if rand == 42:
            msg = 'Hold kæft Laura!'

        if msg is not None:
            await self.bot.send_message(message.channel, msg)

def setup(bot):
    bot.add_cog(Laura(bot))