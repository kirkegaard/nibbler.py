import discord
import logging

from discord.ext import commands

log = logging.getLogger(__name__)

MESSAGES = {
    260858852776476672: [
        'Velkommen {0.mention}. Husk at læse vores regler og nyheder i kanalen til venstre. Husk også at give dig selv til kende med dit BM-brugernavn, så vi ved, hvem du er. Ohøj!',
        'Farvel {0.mention}... TTYN!'
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
        if member.guild.id in MESSAGES:
            msg = MESSAGES[member.guild.id][0].format(member)
            await member.guild.channels[0].send(msg)
            log.info('[member.join] {0.name} {0.mention}'.format(member))

    async def on_member_remove(self, member: discord.Member):
        if member.guild.id in MESSAGES:
            msg = MESSAGES[member.guild.id][1].format(member)
            await member.guild.channels[0].send(msg)
            log.info('[member.join] {0.name} {0.mention}'.format(member))


def setup(bot):
    bot.add_cog(Member(bot))
