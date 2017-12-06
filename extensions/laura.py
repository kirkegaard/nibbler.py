from random import randint
from discord.ext import commands

laura_id = [205282372743069696]


class Laura():

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, ctx):
        # if message.author.id in laura_id and sum(1 for c in message.content if c.isupper()) > 10:
        #     await message.channel.send('Dæmp dig Laura')

        rand = randint(0, 1000)
        msg = None

        if ctx.author.id in laura_id and rand > 900:
            await ctx.add_reaction('\U0001F4A9')


def setup(bot):
    bot.add_cog(Laura(bot))
