import requests
import requests_cache
from discord.ext import commands

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
}


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reddit(self, context, subreddits="", count=1):
        """Fetches a random picture from subreddits."""
        if count > 10:
            await context.send("I can only fetch 10 images. Sorry :(")
            return

        res = []
        for x in range(0, count):
            endpoint = "http://reddit.com/r/{}/random/.json".format(subreddits)

            with requests_cache.disabled():
                data = requests.get(endpoint, headers=headers).json()
                link = data[0]["data"]["children"][0]["data"]["url"]
                if not link in res:
                    res.append(link)

        for y in res:
            await context.send(y)


def setup(bot):
    bot.add_cog(Reddit(bot))
