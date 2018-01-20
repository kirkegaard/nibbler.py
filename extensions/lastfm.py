import requests
import requests_cache
from discord.ext import commands

endpoint = 'http://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&api_key=f5f149ffcdf2e0db0888f6c477c4abc1&user=%s&format=json'

users = {
    163512506269171712 : 'ranza',
    131908822301278208 : 'kawasum1',
    263970974532108288 : 'camillemav',
    249964076132859905 : 'kpthedane1',
    244747185088888832, 'teh_utyske'
}

class LastFM():

    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.content.lower().startswith('hvad hører vi?'):
            if message.author.id in users:
                user = users[message.author.id]
                with requests_cache.disabled():
                    res = requests.get(endpoint % user).json()
                    track = res['recenttracks']['track'][0]
                    artist = track['artist']['#text']
                    title = track['name']
                    await message.channel.send('♫ Vi hører sgu da: **{} - {}**'.format(artist, title))


def setup(bot):
    bot.add_cog(LastFM(bot))

