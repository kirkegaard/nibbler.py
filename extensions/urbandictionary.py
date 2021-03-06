# import urbandictionary as ud
import requests
import discord
from discord.ext import commands


class UrbanDict():

    endpoint = 'http://api.urbandictionary.com/v0/define?term=%s'

    def __init__(self, bot):
        pass

    @commands.command(aliases=['ud'])
    async def urbandict(self, context, *word: str):
        word = ' '.join(word)
        res = requests.get(self.endpoint % word)
        if res.json()['list']:
            definition = res.json()['list'][0]
            await context.channel.send('**{}**: {}\n**Example**: {}'.format(definition['word'], definition['definition'], definition['example']))
        else:
            await context.channel.send('Couldnt find anything on **%s**' % word)


def setup(bot):
    bot.add_cog(UrbanDict(bot))
