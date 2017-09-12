import tvtid
from discord.ext import commands
from fuzzywuzzy import fuzz, process


class Tvtid():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tv(self, context, channel=None):
        if channel is None:
            await context.channel.send('I need to know what channel you want.')
            return

        client = tvtid.Client()
        channels = {k: c.title for k, c in client.channels().items()}
        channel_key = process.extractOne(channel, channels)

        if channel_key is None:
            await context.channel.send('Couldnt find that channel.')
            return

        schedule = client.schedules_for_today([channel_key[2]])[0]
        aired, current, upcoming = schedule.current()

        output = '%s [%s] %s ' % (schedule.channel.title, current.start_time.strftime('%H:%M'), current.title)
        for program in upcoming[:3]:
            output += '[%s] %s ' % (program.start_time.strftime('%H:%M'), program.title)

        await context.channel.send('```%s```' % output)


def setup(bot):
    bot.add_cog(Tvtid(bot))
