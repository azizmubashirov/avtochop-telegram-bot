
def go_message(context, user_id, message, reply_markup=None):
    result = context.bot.send_message(chat_id=user_id, text=message, reply_markup=reply_markup, parse_mode='HTML',
                             disable_web_page_preview=True)
    return result

def send_photo(context, user_id, photo, caption=None, reply_mukup=None):
    try:
        context.bot.send_photo(chat_id=user_id, photo=photo, caption=caption, reply_markup=reply_mukup,
                               parse_mode='HTML')
    except Exception as e:
        print("error send_photo", e)


def send_video(context, user_id, message, video, buttons=None):
    context.bot.send_video(chat_id=user_id, video=video, caption=message, reply_markup=buttons, parse_mode='HTML')


def delete_message_user(context, user_id, message_id):
    context.bot.delete_message(chat_id=user_id, message_id=message_id)


def send_audio(context, user_id, message, audio, buttons=None):
    try:
        context.bot.send_audio(chat_id=user_id, audio=audio, caption=message, reply_markup=buttons,
                               parse_mode='HTML')
    except Exception as e:
        print("error", e)
        
def send_document(context, user_id, file):
    context.bot.send_document(chat_id=user_id, document=file)
    return 1

def edit_message(context, chat_id, message_id, message, reply_markup):
    try:
        context.bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, text=message,
            reply_markup=reply_markup, parse_mode='HTML'
        )
    except Exception as e:
        print('ERROR edit message: ', str(e))

