import discord
import logging
import settings
import sys
from discord.ext import commands
from importlib import import_module, reload


logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix=settings.TRIGGER)


for extension in settings.EXTENSIONS:
    try:
        module = "%s.%s" % (settings.EXTENSION_PATH, extension)

        if module not in sys.modules:
            cog = import_module("." + extension, package=settings.EXTENSION_PATH)
        else:
            cog = reload(sys.modules[module])

        logger.info("Loading extension [%s]", extension)
        cog.setup(bot)
    except Exception as e:
        raise e


bot.run(settings.DISCORD_TOKEN)


# class Nibbler(discord.Client):
#     """Nibbler"""

#     def __init__(self):
#         # self.config = config.Config("config/bot.json")
#         # self.token = self.config["token"]
#         # self.prefix = self.config["prefix"]
#         # self.socket = self.config["socket"]
#         # self.description = self.config["description"]

#         for extension in settings.EXTENSIONS:
#             try:
#                 self.add_cog("extensions." + extension)
#                 print("Loaded extension: {}".format(extension))
#             except Exception as e:
#                 print(f"Failed to load extension {extension}.", file=sys.stderr)
#                 traceback.print_exc()

#     async def on_ready(self):
#         print("Logged on as", self.user)

#     async def on_message(self, message):
#         # don't respond to ourselves
#         if message.author == self.user:
#             return

#         if message.content == "ping":
#             await message.channel.send("pong")

# async def on_command_error(self, ctx, error):
#     if isinstance(error, commands.NoPrivateMessage):
#         await ctx.author.send("This command cannot be used in private messages.")
#     elif isinstance(error, commands.DisabledCommand):
#         await ctx.author.send("Sorry. This command is disabled and cannot be used.")
#     elif isinstance(error, commands.CommandInvokeError):
#         print(f"In {ctx.command.qualified_name}:", file=sys.stderr)
#         traceback.print_tb(error.original.__traceback__)
#         print(
#             f"{error.original.__class__.__name__}: {error.original}",
#             file=sys.stderr,
#         )

#     if self.socket["enabled"]:
#         await self.api.create_server(
#             host=self.socket["host"], port=self.socket["port"]
#         )

# async def on_resumed(self):
#     print("Resumed...")

# async def on_message(self, message):
#     if message.author.bot:
#         return
#     await self.process_commands(message)


# nibbler = Nibbler()
# nibbler.run(settings.DISCORD_TOKEN)
