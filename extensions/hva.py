import re
import collections
from random import randint
from discord.ext import commands


class Hva():

    def __init__(self, bot):
        self.bot = bot
        self.latest = collections.defaultdict(dict)

    async def on_message(self, message):
        if message.author.mention == self.bot.user.mention:
            return

        channel = message.channel.id
        match = re.match(r'^(?i)a?hvad?', message.content)

        if match:
            if not self.latest[channel]:
                return

            await message.channel.send('{} HAN SAGDE: {}'.format(
                message.author.mention,
                self.latest[channel]['content'].upper()))
        else:
            self.latest[channel]['mention'] = message.author.mention
            self.latest[channel]['content'] = message.content


def setup(bot):
    bot.add_cog(Hva(bot))
