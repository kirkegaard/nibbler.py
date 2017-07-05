from discord.ext import commands
from cobe.brain import Brain
import re

brain = Brain("nibbler.brain")

class Brain():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        mention = commands.bot.when_mentioned(self.bot, message).strip()
        if message.author.mention == mention:
            return

        reply = None
        content = re.sub(r'<@.*?>', '', message.content).strip()
        if message.content.startswith(mention):
            while reply == None:
                try:
                    reply = brain.reply(content)
                    await self.bot.send_message(message.channel, '{} {}'.format(message.author.mention, reply))
                except AbortException:
                    return False
                except RetryException:
                    reply = None

        if content and len(content) >= 4:
            print('Learning from: {}'.format(content))
            brain.learn(content)

def setup(bot):
    bot.add_cog(Brain(bot))