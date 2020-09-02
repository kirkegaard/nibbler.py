import requests
import typing
from discord.ext import commands


class Fah(commands.Cog):
    endpoint = "https://stats.foldingathome.org/api/team/{team}"

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fah(self, context, team: typing.Optional[int] = 260640):
        """Look up folding at home stats"""
        res = requests.get(self.endpoint.format(team=team))

        if res.status_code is not 200:
            await context.send("FAH is down :(")
            return

        data = res.json()
        msg = f"TEAM: {data['name']}\n---\n"

        donors = data["donors"][:10]

        rl = max(len(str(r.get("rank", 0))) for r in donors) + 2
        nl = max(len(str(r.get("name", 0))) for r in donors)
        cl = max(len(str(r.get("credit", 0))) for r in donors)

        for donor in donors:
            rank = "[{rank}]".format(rank=donor.get("rank", "NaN")).rjust(rl, " ")
            name = donor.get("name", "NaN").ljust(nl, " ")
            credit = "{credit}".format(credit=donor.get("credit", "0")).ljust(cl, " ")
            msg += "{rank} {name} {credit} ({wus})\n".format(
                rank=rank, name=name, credit=credit, wus=donor.get("wus", "0"),
            )
        await context.send("```%s```" % msg)


def setup(bot):
    bot.add_cog(Fah(bot))
