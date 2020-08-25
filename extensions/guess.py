import random
import asyncio
from discord.ext import commands


class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def guess(self, context):
        message = context.message

        if message.author == self.bot.user:
            return

        await message.channel.send("Guess a number between 1 and 10.")

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await self.bot.wait_for("message", check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(
                "Sorry, you took too long it was {}.".format(answer)
            )

        if int(guess.content) == answer:
            await message.channel.send("You are right!")
        else:
            await message.channel.send("Oops. It is actually {}.".format(answer))


def setup(bot):
    bot.add_cog(Guess(bot))
