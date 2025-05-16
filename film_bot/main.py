"""launching the bot."""

from config import config

from film_bot.bot import Bot

if __name__ == "__main__":
    bot = Bot(config.telegam_bot_token)
    bot.run()
