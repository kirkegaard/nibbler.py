import discord
import logging
from discord.ext import commands

log = logging.getLogger(__name__)

MESSAGES = {
    707606026337255467: {
        "channel_id": 717073908813135962,
        "join": "Velkommen {0.mention}! Møz :*",
        "leave": "Favle {0.mention}... TTYN!",
    },
    312288797197074432: {
        "channel_id": 312288797197074432,
        "join": "Hva så?",
        "leave": "Sæs...",
    },
}


class ChannelEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def trigger(self, member, msg):
        if member.guild.id not in MESSAGES:
            return

        data = MESSAGES[member.guild.id]
        channel = member.guild.get_channel(data["channel_id"])
        msg = data[msg].format(member)

        await channel.send(msg)

        log.info("[member.{msg}] {0.name} {0.mention}".format(member))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.trigger(member, "join")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.trigger(member, "leave")


def setup(bot):
    bot.add_cog(ChannelEvents(bot))
