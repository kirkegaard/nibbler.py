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
