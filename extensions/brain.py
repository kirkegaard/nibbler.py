from discord.ext import commands
from cobe.brain import Brain
import re
import discord

brain = Brain("tmp/nibbler.brain")
# the channels we want the bot to learn from
channels = [260858852776476672]


class Brain():

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        is_private = isinstance(message.channel, discord.abc.PrivateChannel)

        if message.author.mention == self.bot.user.mention or message.content.startswith('!'):
            return

        reply = None
        content = re.sub(r'<@.*?>', '', message.content).strip()
        if message.content.startswith(self.bot.user.mention) or is_private:
            while reply == None:
                try:
                    reply = brain.reply(content)
                    if is_private:
                        await message.channel.send(reply)
                    else:
                        await message.channel.send(f'{message.author.mention} {reply}')
                except AbortException:
                    return False
                except RetryException:
                    reply = None

        if len(content) >= 4 and message.channel.id in channels:
            print('Learning from: {}'.format(content))
            brain.learn(content)


def setup(bot):
    bot.add_cog(Brain(bot))
