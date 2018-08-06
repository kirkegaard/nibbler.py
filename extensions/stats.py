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

    @commands.command(aliases=['sts'])
    async def stats(self, context, channel=None):
        if not channel:
            channel = context.channel.id

        gid = context.guild.id
        cid = context.channel.id

        cur = self.conn.cursor()
        cur.execute('SELECT * FROM users WHERE gid = ? AND cid = ? ORDER BY count DESC', [gid, cid])

        output = []
        for idx, row in enumerate(cur.fetchall()):
            c = idx + 1
            output.append('{}. {}: {}'.format(c, row['username'], row['count']))

        await context.send('```\n%s```' % '\n'.join(output))


def setup(bot):
    bot.add_cog(Stats(bot))
