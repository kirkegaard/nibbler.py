import discord
import re

from utils import config as db
from datetime import datetime
from discord.ext import commands

class Url():

    def __init__(self, bot):
        self.bot = bot
        self.db = db.Config('tmp/urls.json')

    async def on_message(self, context):
        if context.author.bot:
            return

        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', context.content)
        for url in urls:
            check = self.db.get(url)

            if check:
                await context.channel.send('OFN, {} said it @ {}'.format(check['user'], check['date']))
                return

            data = {
                'user': context.author.mention,
                'date': datetime.now().strftime('%d. %b @ %H:%M')
            }
            await self.db.put(url, data)

def setup(bot):
    bot.add_cog(Url(bot))
