import discord
import logging

from discord.ext import commands

log = logging.getLogger(__name__)

MESSAGES = {
    483727087903965194: [
        'Velkommen {0.mention}. Husk at læse vores regler og nyheder! Møz :*',
        'Favle {0.mention}... TTYN!'
    ],
    312288797197074432: [
        'Hva så?',
        'Sæs'
    ]
}


class Member():

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member: discord.Member):
        mid = member.guild.id
        if mid in MESSAGES:
            msg = MESSAGES[mid][0].format(member)
            channel = self.bot.get_channel(mid)
            await channel.send(msg)
            log.info('[member.join] {0.name} {0.mention}'.format(member))

    async def on_member_remove(self, member: discord.Member):
        mid = member.guild.id
        if mid in MESSAGES:
            msg = MESSAGES[mid][1].format(member)
            channel = self.bot.get_channel(mid)
            await channel.send(msg)
            log.info('[member.join] {0.name} {0.mention}'.format(member))

def setup(bot):
    bot.add_cog(Member(bot))
