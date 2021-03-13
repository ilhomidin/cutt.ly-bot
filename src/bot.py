import os

import telebot

import url_shortener


bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"], parse_mode=None)


def shorten(url: str) -> str:
    return url_shortener.shorten(os.environ["CUTTLY_API_KEY"], url)


@bot.message_handler(content_types=["text"])
def short_link(message: telebot.types.Message):
    answer = shorten(message.text)
    bot.reply_to(message, answer)


if __name__ == "__main__":
    bot.polling()
