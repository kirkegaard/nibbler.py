import discord
import logging
import pprint

from utils import config as db
from datetime import datetime
from discord.ext import commands

log = logging.getLogger(__name__)


class Notify():

    def __init__(self, bot):
        self.bot = bot
        self.db = db.Config('tmp/notifications.json')

    async def on_message(self, context):
        notifications = self.db.get(context.author.mention)
        if notifications is None:
            return

        for n in notifications:
            await context.author.send("[notification]: {} ({}) wrote: {}".format(
                n['member'], n['date'], n['msg']))

        await self.db.put(context.author.mention, [])

    @commands.command()
    async def notify(self, context, member, *msg: str):
        """Adds a notification for the next time the user is online"""
        if member is self.bot.user.mention:
            return

        data = {
            "member": member,
            "msg": ' '.join(msg),
            "date": datetime.now().strftime('%d. %b %H:%M')
        }

        notifications = self.db.get(member)
        if notifications is None:
            notifications = []

        notifications.append(data)

        await self.db.put(member, notifications)
        await context.channel.send(f"Roger! Sending him/her a notification")


def setup(bot):
    bot.add_cog(Notify(bot))
