import asyncio
from datetime import datetime, timedelta
from discord.ext import commands


class Timer(commands.Cog):
    def __init__(self, bot, loop=None):
        self.bot = bot
        self.loop = loop or asyncio.get_event_loop()

    @commands.command(
        aliases=["alarm", "timer"],
        pass_context=True,
        description="Sends you a reminder at a given time. Use the time format hh:mm",
    )
    async def alert(self, context, time, *message):
        """Get a reminder"""
        time = list(map(int, time.split(":")))

        now = datetime.now()
        then = now.replace(hour=time[0], minute=time[1])
        later = then - now
        message = " ".join(message)

        if then < now:
            await context.send(
                "{} Sorry, thats in the past!".format(context.message.author.mention)
            )
            return

        await context.send("{} I got you fam!".format(context.message.author.mention))

        def send():
            asyncio.ensure_future(context.message.author.send(message), loop=self.loop)

        self.loop.call_at(self.loop.time() + later.seconds, send)


def setup(bot):
    bot.add_cog(Timer(bot))
