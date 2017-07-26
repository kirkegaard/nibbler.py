import discord
import logging

from utils import config
from discord.ext import commands

log = logging.getLogger(__name__)
config = config.Config('config/bot.json')
ROLES = config.get('roles')


class ActionReason(commands.Converter):
    async def convert(self, context, argument):
        res = f'{context.author} ({context.author.id}): {argument}'

        if len(res) > 512:
            reason_max = 512 - len(res) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return res


class MemberID(commands.Converter):
    async def convert(self, context, argument):
        try:
            member = await commands.MemberConverter().convert(context, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            can_execute = context.author.id == context.bot.owner_id or \
                context.author == context.guild.owner

            if not can_execute:
                raise commands.BadArgument(
                    'You cannot do this action on this user due to role hierarchy.')
            return member.id


class BannedMember(commands.Converter):
    async def convert(self, context, argument):
        ban_list = await context.guild.bans()
        try:
            member_id = int(argument, base=10)
            entity = discord.utils.find(
                lambda u: u.user.id == member_id, ban_list)
        except ValueError:
            entity = discord.utils.find(
                lambda u: str(u.user) == argument, ban_list)

        if entity is None:
            raise commands.BadArgument("Couldnt find member")
        return entity


class Moderator():
    """
    A lot of these parts are borrowed/inspired by the awesome RoboDanny
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(no_pm=True)
    @commands.has_any_role(*ROLES['admin'])
    async def kick(self, context, member: discord.Member, *, reason: ActionReason=None):
        """Kicks a user from the server"""
        if reason is None:
            reason = f'Kicked by {context.author} ({context.author.id})'

        await member.kick(reason=reason)
        await context.send('\N{OK HAND SIGN}')

    @commands.command(no_pm=True)
    @commands.has_any_role(*ROLES['admin'])
    async def ban(self, context, member: MemberID, *, reason: ActionReason=None):
        """Bans a user from the server"""
        if reason is None:
            reason = f'Banned by {context.author} ({context.author.id})'

        await context.guild.ban(discord.Object(id=member), reason=reason)
        await context.send('\N{OK HAND SIGN}')

    @commands.command(no_pm=True)
    @commands.has_any_role(*ROLES['admin'])
    async def unban(self, context, member: BannedMember, *, reason: ActionReason=None):
        """Unbans a member from the server."""
        if reason is None:
            reason = f'Unbanned by {context.author} ({context.author.id})'

        await context.guild.unban(member.user, reason=reason)
        await context.send(f'\N{OK HAND SIGN}')


def setup(bot):
    bot.add_cog(Moderator(bot))
