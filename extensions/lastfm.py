import requests
import requests_cache
from discord.ext import commands


ENDPOINT = "http://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&api_key=f5f149ffcdf2e0db0888f6c477c4abc1&user=%s&format=json"
USERS = {
    163512506269171712: "ranza",
    263970974532108288: "camillemav",
}


class LastFM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith("hvad hører vi?"):
            if message.author.id in USERS:
                user = USERS[message.author.id]
                with requests_cache.disabled():
                    res = requests.get(ENDPOINT % user).json()
                    track = res["recenttracks"]["track"][0]
                    artist = track["artist"]["#text"]
                    title = track["name"]
                    await message.channel.send(
                        "♫ Vi hører sgu da: **{} - {}**".format(artist, title)
                    )
            else:
                await message.channel.send("Aner det ikke!")


def setup(bot):
    bot.add_cog(LastFM(bot))
