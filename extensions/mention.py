import discord
from discord.ext import commands
from utils import config as db


class Mention():

    def __init__(self, bot):
        self.bot = bot
        self.db = db.Config('tmp/mention.json')

    @commands.group()
    async def mention(self, context):
        """Mention sends you notifications when a word appear in a message.
        It will only notify you if your status is set to offline!"""
        if context.invoked_subcommand is None:
            await context.send('Use `!mention add [word]` to add a word. Or use `!mention del [word]` to delete a word.')

    @mention.command()
    async def list(self, context):
        """Lists all the words im notifying you on."""
        mentions = self.db.get(context.author.id) or None
        if mentions is None:
            await context.send('Dont have any mentions on you')
            return

        await context.send('Ive got: **"{}"** on you'.format(', '.join(mentions)))


    @mention.command()
    async def add(self, context, *word: str):
        """Adds a new word to your list."""
        mentions = self.db.get(context.author.id) or []

        word = ' '.join(word).lower()

        if word in mentions:
            await context.send('Already got that word');
            return

        mentions.append(word)

        await self.db.put(context.author.id, mentions)
        await context.send('Added {} to {}'.format(word, context.author.mention));

    @mention.command(aliases=['del'])
    async def delete(self, context, *word: str):
        """Deletes a word from your list."""
        mentions = self.db.get(context.author.id) or None
        if mentions is None:
            await context.send('Dont have any mentions on you')
            return

        word = ' '.join(word).lower()

        mentions.remove(word)

        await self.db.put(context.author.id, mentions)
        await context.send('Removed {} from {}'.format(word, context.author.mention));


    async def on_message(self, context):
        is_private = isinstance(context.channel, discord.abc.PrivateChannel)
        if is_private or context.author.mention == self.bot.user.mention or context.content.startswith('!mention'):
            return

        all = self.db.all()
        for user in self.db.all():
            for word in all[user]:
                if word in context.content.lower():
                    if int(user) == context.author.id:
                        break

                    res = context.guild.get_member(int(user))
                    if res and str(res.status) == 'offline':
                        print('[Mention] Sending notification')
                        await res.send('{} mentioned you: {}'.format(context.author.mention, context.content))
                        break

def setup(bot):
    bot.add_cog(Mention(bot))
