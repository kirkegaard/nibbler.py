import sqlite3
from discord.ext import commands
from utils import config

conf = config.Config('config/bot.json')
ROLES = conf.get('roles')


class Subscriptions():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')
        self.conn = sqlite3.connect(self.config.get('subscription_db'))
        self.conn.row_factory = sqlite3.Row

    @commands.group()
    async def subscriptions(self, context):
        if context.invoked_subcommand is None:
            await context.send('Use `!subscriptions add [subreddit]` or `!subscriptions del [subreddit]`')

    @subscriptions.command(aliases=['add', 'sub'])
    @subscriptions.has_any_role(*ROLES['admin'])
    async def add(self, context, subreddit, channel=None):
        if not channel:
            channel = context.channel.id

        cur = self.conn.cursor()
        res = cur.execute('INSERT INTO subscriptions VALUES (0,?,?)', [channel, subreddit])
        self.conn.commit()

        await context.send('Subreddit added to channel')

    @subscriptions.command(aliases=['del', 'unsub'])
    @subscriptions.has_any_role(*ROLES['admin'])
    async def delete(self, context, subreddit, channel=None):
        if not channel:
            channel = context.channel.id

        cur = self.conn.cursor()
        res = cur.execute('DELETE FROM subscriptions WHERE channel = ? AND subreddit = ?', [channel, subreddit])
        self.conn.commit()

        await context.send('Subreddit removed from channel')

    @subscriptions.command(aliases=['list', 'subs'])
    async def list(self, context, channel=None):
        if not channel:
            channel = context.channel.id

        cur = self.conn.cursor()
        res = cur.execute('SELECT subreddit FROM subscriptions WHERE channel = ? ORDER BY subreddit', [channel])
        subs = []

        for row in res:
            subs.append(row['subreddit'])
        await context.send('```\n%s```' % '\n'.join(subs))


def setup(bot):
    bot.add_cog(Subscriptions(bot))
