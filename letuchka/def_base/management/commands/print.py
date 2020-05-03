
def do_print(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    input_text = update.message.text

