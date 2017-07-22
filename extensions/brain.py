from discord.ext import commands
from cobe.brain import Brain
import re

brain = Brain("tmp/nibbler.brain")
# the channels we want the bot to learn from
channels = [260858852776476672]


class Brain():

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author.mention == self.bot.user.mention or message.content.startswith('!'):
            return

        reply = None
        content = re.sub(r'<@.*?>', '', message.content).strip()
        if message.content.startswith(self.bot.user.mention):
            while reply == None:
                try:
                    reply = brain.reply(content)
                    await message.channel.send('{} {}'.format(message.author.mention, reply))
                except AbortException:
                    return False
                except RetryException:
                    reply = None

        if len(content) >= 4 and message.channel.id in channels:
            print('Learning from: {}'.format(content))
            brain.learn(content)


def setup(bot):
    bot.add_cog(Brain(bot))
