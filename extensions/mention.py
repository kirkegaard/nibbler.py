import discord
from discord.ext import commands
from utils import config as db


class Mention():

    def __init__(self, bot):
        self.bot = bot
        self.db = db.Config('tmp/mention.json')

    @commands.group()
    async def mention(self, context):
        if context.invoked_subcommand is None:
            await context.send('Use !mention add [word] to add a word. Or use !mention delete [word] to remove a word')

    @mention.command()
    async def list(self, context):
        mentions = self.db.get(context.author.id) or None
        if mentions is None:
            await context.send('Dont have any mentions on you')

        await context.send('Ive got: **"{}"** on you'.format(', '.join(mentions)))


    @mention.command()
    async def add(self, context, *word: str):
        mentions = self.db.get(context.author.id) or []

        word = ' '.join(word)

        if word in mentions:
            await context.send('Already got that word');
            return

        mentions.append(word)

        await self.db.put(context.author.id, mentions)
        await context.send('Added {} to {}'.format(word, context.author.mention));

    @mention.command()
    async def delete(self, context, *word: str):
        pass


    async def on_message(self, context):
        is_private = isinstance(context.channel, discord.abc.PrivateChannel)
        if is_private or context.author.mention == self.bot.user.mention:
            return

        all = self.db.all()
        for user in self.db.all():
            if any(word in context.content for word in all[user]):
                u = await self.bot.get_user_info(user)
                if u:
                    await u.send('{} mentioned you: {}'.format(context.author.mention, context.content))
                    return

def setup(bot):
    bot.add_cog(Mention(bot))
