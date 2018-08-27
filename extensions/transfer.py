import re
import requests
import discord
from discord.ext import commands


class Transfer():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def transfer(self, context, channel: int):
        channel = self.bot.get_channel(channel)

        async for msg in channel.history(limit=100000000000000, reverse=True):
            date = msg.created_at.strftime("%Y-%m-%d %H:%M")
            try:
                author = msg.author.mention
            except:
                author = 'invalid'

            res = '[{}] {} : {}'.format(date, author, msg.content)
            await context.channel.send(res)


def setup(bot):
    bot.add_cog(Transfer(bot))
