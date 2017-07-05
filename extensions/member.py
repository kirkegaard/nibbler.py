import discord
from discord.ext import commands
import logging

log = logging.getLogger(__name__)
client = discord.Client()

class Member():
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member : discord.Member):
        msg = 'Velkommen {0.mention}. Husk at læse vores regler og nyheder i kanalen til venstre. Husk også at give dig selv til kende med dit BM-brugernavn, så vi ved, hvem du er. Ohøj!'
        await self.bot.send_message(member.server.default_channel, msg.format(member))
        log.info('[member.join] {0.name} {0.mention}'.format(member))

    async def on_member_remove(self, member : discord.Member):
        msg = 'Farvel {0.mention}... TTYN!'
        await self.bot.send_message(member.server.default_channel, msg.format(member))
        log.info('[member.remove] {0.name} {0.mention}'.format(member))

def setup(bot):
    bot.add_cog(Member(bot))