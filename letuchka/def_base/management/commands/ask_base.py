from .bases import profile, write_to_category
from telegram.ext import Filters, MessageHandler, Updater


def do_print(update: Updater, context):
    p, _ = profile(update, update.message.chat_id)

    """Echo the user message."""
    update.message.reply_text(update.message.text)
    input_text = update.message.text
    write_to_category(p, input_text)
    return MessageHandler.END


def get_answer(updater, update):
    update.message.reply_text("Введте название категории")
    updater.dispatcher.add_handler(MessageHandler(Filters.text, do_print))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
