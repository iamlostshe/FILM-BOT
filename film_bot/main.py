"""launching the bot."""

from config import config
from DoranimeBot import DoranimeBot

if __name__ == "__main__":
    bot = DoranimeBot(config.telegam_bot_token)
    bot.run()
