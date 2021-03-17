import os

import telebot

import url_shortener


bot = telebot.TeleBot(os.environ["TELEGRAM_BOT_TOKEN"], parse_mode=None)


def shorten(url: str) -> str:
    """Partial url_shortener.shorten function
    Load api_key from environ
    """
    return url_shortener.shorten(os.environ["CUTTLY_API_KEY"], url)


@bot.message_handler(commands=["start", "help"])
def howto(message: telebot.types.Message):
    """Send howto message"""
    bot.send_message(
        message.chat.id, "👋 Hi, send me a link and I will try to shorten it!"
    )


@bot.message_handler(content_types=["text"])
def short_link(message: telebot.types.Message):
    """Shorten given link"""
    idler = bot.reply_to(message, "👌 OK. Wait a faw seconds")
    bot.send_chat_action(message.chat.id, "typing", 2)
    answer = shorten(message.text)
    bot.edit_message_text(answer, message.chat.id, idler.message_id)


if __name__ == "__main__":
    bot.polling()
