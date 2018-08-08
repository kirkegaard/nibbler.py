import discord
import sqlite3
from discord.ext import commands
from utils import config
from datetime import datetime


class Stats():

    def __init__(self, bot):
        self.bot = bot
        self.config = config.Config('config/bot.json')
        self.conn = sqlite3.connect(self.config.get('stats_db'))
        self.conn.row_factory = sqlite3.Row

    async def on_message(self, context):
        if context.author.bot or isinstance(context.channel, discord.channel.DMChannel):
            return

        gid = context.guild.id
        cid = context.channel.id
        uid = context.author.id
        user = context.author.name
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users WHERE gid = ? AND cid = ? AND uid = ?', [gid, cid, uid])
        row = cur.fetchone()
        if row:
            count = row['count'] + 1
            cur.execute('UPDATE users SET count = ?, date = ? WHERE gid = ? AND cid = ? AND uid = ?',
                        [count, date, gid, cid, uid])
        else:
            cur.execute('INSERT INTO users (count, date, gid, cid, uid, username) VALUES (1,?,?,?,?,?)',
                        [date, gid, cid, uid, user])
        self.conn.commit()

    @commands.group()
    async def stats(self, context):
        if context.invoked_subcommand is not None:
            return

        cid = context.channel.id
        gid = context.guild.id

        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users WHERE gid = ? AND cid = ? ORDER BY count DESC LIMIT 10', [gid, cid])
        await self.say(context, cur.fetchall())

    @stats.command()
    async def guild(self, context, gid=None):
        if not gid:
            gid = context.guild.id

        cur = self.conn.cursor()
        cur.execute('SELECT username, sum(count) as count FROM users WHERE gid=? GROUP BY username ORDER BY count DESC LIMIT 10', [gid])
        await self.say(context, cur.fetchall())

    async def say(self, context, rows):
        output = []
        for idx, row in enumerate(rows):
            c = idx + 1
            output.append('{}. {}: {}'.format(c, row['username'], row['count']))
        await context.send('```\n%s```' % '\n'.join(output))


def setup(bot):
    bot.add_cog(Stats(bot))
