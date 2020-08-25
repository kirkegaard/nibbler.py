import discord
from discord.ext import commands
from currency_converter import CurrencyConverter
import numexpr


class Calc():

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, context, *, message: str):
        if 'in' in message:
            s = message.upper().split(' ')
            c = CurrencyConverter()
            res = c.convert(s[0], s[1], s[3])
            await context.send(res)
        res = numexpr.evaluate(message)
        await context.send(res.item())


def setup(bot):
    calc = Calc(bot)
    bot.add_cog(calc)
