import os

import telebot


bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"], parse_mode=None)


if __name__ == "__main__":
    bot.polling()
