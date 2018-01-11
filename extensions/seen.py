import discord
from utils import config as db
from datetime import datetime
from discord.ext import commands

class Seen():

    def __init__(self, bot):
        self.bot = bot
        self.db = db.Config('tmp/seen.json')

    @commands.command()
    async def seen(self, context, user: str):
        res = self.db.get(user)
        if res is None:
            await context.channel.send('Havent seen that guy around')
            return

        await context.channel.send("I last saw {} in #{} on {} saying: {}".format(
            user, res['channel'], res['date'], res['msg']))

    async def on_message(self, context):
        if context.author.bot:
            return
        user = self.db.get(context.author.mention)
        date = datetime.now().strftime('%d. %b @ %H:%M')

        if isinstance(context.channel, discord.channel.DMChannel):
            channel = 'Private'
            msg = '***'
        else:
            channel = context.channel.name
            msg = context.content

        data = {
            "date": date,
            "channel": channel,
            "msg": msg
        }

        await self.db.put(context.author.mention, data)

def setup(bot):
    bot.add_cog(Seen(bot))

