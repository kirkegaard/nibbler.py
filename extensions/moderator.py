import discord
from discord.ext import commands
import logging

log = logging.getLogger(__name__)


class Moderator():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    async def kick(self, *, member: discord.Member):
        try:
            await self.bot.kick(member)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to kick this member.')
        except discord.HTTPException:
            await self.bot.say('Kicking failed.')
        else:
            await self.bot.say('\U0001f44c')

    @commands.command(no_pm=True)
    async def ban(self, *, member: discord.Member):
        try:
            await self.bot.ban(member)
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to ban this member.')
        except discord.HTTPException:
            await self.bot.say('Banning failed.')
        else:
            await self.bot.say('\U0001f44c')

    # This is kind of wonky since it requires the users id
    # We need to figure out a way to find the user easier
    @commands.command(pass_context=True, no_pm=True)
    async def unban(self, context, member_id):
        try:
            await self.bot.unban(context.message.server, discord.Object(member_id))
        except discord.Forbidden:
            await self.bot.say('The bot does not have permissions to unban this member.')
        except discord.HTTPException:
            await self.bot.say('Unbanning failed.')
        else:
            await self.bot.say('\U0001f44c')


def setup(bot):
    bot.add_cog(Moderator(bot))
