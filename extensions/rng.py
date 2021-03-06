import random
from discord.ext import commands

EIGHTBALL = [
    'It is certain',
    'It is decidedly so',
    'Without a doubt',
    'Yes definitely',
    'You may rely on it',
    'As I see it, yes',
    'Most likely',
    'Outlook good',
    'Yes',
    'Signs point to yes',
    'Reply hazy try again',
    'Ask again later',
    'Better not tell you now',
    'Cannot predict now',
    'Concentrate and ask again',
    'Don\'t count on it',
    'My reply is no',
    'My sources say no',
    'Outlook not so good',
    'Very doubtful'
]


class RNG():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    async def eightball(self, context, question: str):
        """Ask the magic 8 ball anything"""
        await context.send(random.choice(EIGHTBALL))

    @commands.command()
    async def roll(self, context, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await context.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await context.send(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, context, *choices: str):
        """Chooses between multiple choices."""
        await context.send(random.choice(choices))


def setup(bot):
    bot.add_cog(RNG(bot))
