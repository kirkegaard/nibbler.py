import re
from discord.ext import commands
from cobe.brain import Brain


brain = Brain("tmp/nibbler.brain")


class Brain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content.startswith("!"):
            return

        reply = None
        content = re.sub(r"<@.*?>", "", message.content).strip()
        if self.bot.user in message.mentions:
            while reply == None:
                try:
                    reply = brain.reply(content)
                    await message.channel.send(f"{message.author.mention} {reply}")
                except AbortException:
                    return False
                except RetryException:
                    reply = None

        if len(content) >= 4:
            print("Learning from: {}".format(content))
            brain.learn(content)


def setup(bot):
    bot.add_cog(Brain(bot))
