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

    @commands.command(aliases=['sub'])
    @commands.has_any_role(*ROLES['admin'])
    async def subscribe(self, context, subreddit, channel=None):
        if not channel:
            channel = context.channel.id

        cur = self.conn.cursor()
        res = cur.execute('INSERT INTO subscriptions VALUES (0,?,?)', [channel, subreddit])
        self.conn.commit()

        await context.send('Subreddit removed from channel')

    @commands.command(aliases=['unsub'])
    @commands.has_any_role(*ROLES['admin'])
    async def unsubscribe(self, context, subreddit, channel=None):
        if not channel:
            channel = context.channel.id

        cur = self.conn.cursor()
        res = cur.execute('DELETE FROM subscriptions WHERE channel = ? AND subreddit = ?', [channel, subreddit])
        self.conn.commit()

        await context.send('Subreddit removed from channel')

    @commands.command(aliases=['subs'])
    async def subscriptions(self, context, channel=None):
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
