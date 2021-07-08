import os
import uuid

import telegram

import url_shortener


def shorten(url: str) -> str:
    """
    Partial url_shortener.shorten function
    Load api_key from environ
    """
    return url_shortener.shorten(os.environ["CUTTLY_API_KEY"], url)


def howto(upd: telegram.Update, _):
    """Send howto message"""
    upd.message.reply_text(
        "👋 Hi, send me a link and I will try to shorten it!"
    )


def short_link(upd: telegram.Update, _):
    """Shorten given link"""
    if upd.message:
        idler = upd.message.reply_text("👌 OK. Wait a faw seconds.", quote=True)
        upd.message.reply_chat_action("typing", 2)
        try:
            answer = shorten(upd.message.text)
        except Exception as exc:
            answer = exc.args[0]
        upd.message.bot.edit_message_text(
            chat_id=idler.chat.id,
            message_id=idler.message_id,
            text=answer,
            disable_web_page_preview=True,
        )
    elif upd.inline_query and upd.inline_query.query:
        try:
            answer = shorten(upd.inline_query.query)
        except Exception as exc:
            answer = exc.args[0]
        upd.inline_query.answer(
            [
                telegram.InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Cutt.ly bot",
                    description=answer,
                    input_message_content=telegram.InputTextMessageContent(
                        answer,
                        disable_web_page_preview=True,
                    ),
                )
            ]
        )


if __name__ == "__main__":
    from telegram import ext

    updater = ext.Updater(os.environ["TELEGRAM_BOT_TOKEN"])
    dispatcher = updater.dispatcher
    dispatcher.add_handler(ext.CommandHandler("start", howto))
    dispatcher.add_handler(ext.CommandHandler("help", howto))
    dispatcher.add_handler(ext.MessageHandler(ext.Filters.text, short_link))
    dispatcher.add_handler(ext.InlineQueryHandler(short_link))

    updater.start_polling()
    updater.idle()
