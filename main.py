import logging
import sys

import discord

from bot import bot
import env

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == "__main__":
    bot.run(env.DISCORD_TOKEN)
