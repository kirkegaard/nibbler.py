import re
import requests
import discord
from discord.ext import commands

class Wttr():

    def __init__(self, bot):
        pass

    @commands.command(aliases=['w', 'weather'])
    async def wttr(self, context, *location: str):
        r = requests.get('https://wttr.in/%s?1nT' % '+'.join(location))
        if r.status_code == 200:
            w = re.sub(r'\s+(New feature.*|Follow.*)\s*$', '', r.text, flags=re.M)
            await context.channel.send('```%s```' % w)

def setup(bot):
    bot.add_cog(Wttr(bot))

