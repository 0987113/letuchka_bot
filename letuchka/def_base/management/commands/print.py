
def do_print(update, context):
    print('do_print')
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    input_text = update.message.text
    print('input_text', input_text)

