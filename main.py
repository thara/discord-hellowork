import logging
import sys

import discord

from bot import bot
import env

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    bot.run(env.DISCORD_TOKEN)
