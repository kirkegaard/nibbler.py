import urbandictionary as ud
import discord
from discord.ext import commands

class UrbanDict():

    def __init__(self, bot):
        pass

    @commands.command(aliases=['ud'])
    async def urbandict(self, context, *subject: str):
        defs = ud.define(' '.join(subject))
        if defs:
            await context.channel.send(defs[0].definition)

def setup(bot):
    bot.add_cog(UrbanDict(bot))

