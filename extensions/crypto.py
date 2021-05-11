import requests
import requests_cache
from discord.ext import commands
from os import environ


class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["c"])
    async def crypto(self, context, *query: str):
        """Tells the price of a crypto coin"""
        res = requests.get(
            "https://api.nomics.com/v1/currencies/ticker",
            params={
                "key": environ.get("NOMICS_KEY"),
                "ids": "".join(query).upper(),
                "interval": "1h,1d,7d",
                "convert": "DKK",
                "per-page": 100,
                "page": 1,
            },
        )

        out = ""
        tpl = "{name} (**{symbol}**) is currently trading at **{price} DKK** (1 Hour Change: **{change_1h}%** 24 Hour Change: **{change_1d}%** 7 Day Change: **{change_7d}%**)\n"

        for c in res.json():
            out += tpl.format(
                name=c["name"],
                symbol=c["symbol"],
                price=c["price"],
                change_1h=c["1h"]["price_change_pct"],
                change_1d=c["1d"]["price_change_pct"],
                change_7d=c["7d"]["price_change_pct"],
            )
        await context.send(out)


def setup(bot):
    bot.add_cog(Crypto(bot))
