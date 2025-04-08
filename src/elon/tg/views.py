from django.shortcuts import render

from telegram import ReplyMarkup, bot, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardRemove, InputMediaPhoto, BotCommand, WebAppInfo

from elon.users.models import User
from .userdata import UserLog
from .sends import *
from elon.tg.create.reg import RegisterView
from datetime import timedelta, datetime
import re
import random
import string
from django.conf import settings

BUTTON = [
    "🇺🇿 Uz",
    "🇷🇺 Ru",
]
BUTTON1 = {
    "ads_create":{
        1: "E'lon qo'shish",
        2: "Oбъявления создают"
    },
    'ads_view': {
        1: "E'lon ko'rish",
        2: "Посмотреть объявление"
    },
    "my_ads":{
        1: "Mening e'lonlarim",
        2: "Мои объявления"
    },
    "settings":{
        1: "Sozlamalar",
        2: "Настройки"
    },
    "favourite_ads": {
        1: "Sevimli e'lonlar",
        2: "Избранные объявления"
    }
}

def start(update, context):
    user_data = update.message.from_user
    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()

    channel_id = ""
    user_id = update.message.from_user.id
    try:
        channel_check = context.bot.get_chat_member(channel_id, user_id)
        if channel_check and channel_check.status != "left":
            user = User.objects.filter(chat_id=user_data.id).first()
            if not user:
                message = f"Assalomu alaykum <a href='tg://user?id={user_data.id}'>{user_data.first_name or '----'}</a> tilni tanlang\n"
                go_message(context=context, user_id=user_data.id, message=message,
                        reply_markup=ReplyKeyboardMarkup([[BUTTON[0], BUTTON[1]]], one_time_keyboard=False, resize_keyboard=True))
                return 1
    
            else:
                menu(user_data.id, user_state.get('lang_id'), context)
        else:
            text = "Подпишитесь на наш канал и отправьте команду /start, вы сможете полноценно использовать бота\n\nKanalimizga obuna bo'ling va /start buyrug'ini yuboring, botdan to'liq foydalana olasiz"
            button = [
                    [
                    InlineKeyboardButton("A'zo bo'lish ✅", url=f""),
                    ]
                ]
    
            go_message(context=context, user_id=user_data.id, message=text,
                            reply_markup=InlineKeyboardMarkup(button))
    except:
        print("erroor")
        text = "Подпишитесь на наш канал и отправьте команду /start, вы сможете полноценно использовать бота\n\nKanalimizga obuna bo'ling va /start buyrug'ini yuboring, botdan to'liq foydalana olasiz"
        button = [
                [
                InlineKeyboardButton("A'zo bo'lish ✅", url=f""),
                ]
            ]
    
        go_message(context=context, user_id=user_data.id, message=text,
                        reply_markup=InlineKeyboardMarkup(button))

def menu(user_id, lang, context):
    user = User.objects.filter(chat_id=user_id).first()
    ads_create = WebAppInfo(f"") 
    ads_view = WebAppInfo(f"") 
    favourite_ads = WebAppInfo(f"") 
    my_ads = WebAppInfo(f"") 
    button = [
        [KeyboardButton(BUTTON1['ads_create'][lang], web_app=ads_create), KeyboardButton(BUTTON1['ads_view'][lang], web_app=ads_view)],
        [KeyboardButton(BUTTON1['favourite_ads'][lang], web_app=favourite_ads), KeyboardButton(BUTTON1['my_ads'][lang], web_app=my_ads)]
    ]
    message = "<b>Avtopik</b> ga xush kelibsiz!\n\n<b>Kerakli bo‘limni tanlang:</b>👇" if lang == 1 else "Добро пожаловать в <b>Avtopik</b>!\n\n<b>Выберите нужный раздел:</b>👇"
    go_message(context=context, user_id=user_id, message=message,
               reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=False, resize_keyboard=True))

def message_handler(update, context):
        user_data = update.message.from_user
        text = update.message.text

        user_log = UserLog(user_data.id)
        user_state = user_log.get_log()

        if text == BUTTON[0]:
            user_state.update({'menu_state': 1, 'state': 100, 'lang_id': 1})
            user_log.change_log(user_state)
        elif text == BUTTON[1]:
            user_state.update({'menu_state': 1, 'state': 100, 'lang_id': 2})
            user_log.change_log(user_state)

        state = user_state.get('state', 0)
        menu_state = user_state.get('menu_state', 0)

        if menu_state == 1 or menu_state == 2:
            reg = RegisterView(user_data.id)
            reg.message_handler(context, update, text, user_data)

def contact_handler(update, context):
    user_data = update.message.from_user
    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()

    contact = update.message.contact.phone_number
    phone_number = check_phone_number(contact)
    if phone_number and phone_number[1]:
        user = User.objects.filter(phone_number=phone_number[0]).first()
        if not user:
            user_state.update({'state': 103})
            sms_code = ''.join(random.choice(string.digits) for _ in range(4))
            user_state['contact'] = {'phone_number': phone_number[0], 'code': sms_code}
            user_log.change_log(user_state)
            message = f"<b>Tasdiqlash kodini kiriting:</b> {sms_code}"
            go_message(context=context, user_id=user_data.id,  message=message)
        else:
            message = f"<b>❌ Xato</b>\n\n Bu telefon raqam oldin ro'yxatan o'tgan" if user_state.get('lang_id') == 1 else f"<b>❌ Ошибка</b>\n\n Этот номер телефона уже зарегистрирован"
            go_message(context, user_id=user_data.id, message=message)
    else:
        message = f"<b>❌ Xato</b>\n\n Telefon raqamingizni to'g'ri kiriting!"
        go_message(context, user_id=user_data.id, message=message)

def callback_handler(update, context):
    query = update.callback_query
    user_data = query.from_user
    message_id = query.message.message_id
    data_sp = query.data.split('#')

    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()


def photo_handler(update, context):
    user_data = update.message.from_user
    file_id = update.message.photo[-1].file_id

    user_log = UserLog(user_data.id)
    user_state = user_log.get_log()
    user = User.objects.filter(tg_id=user_data.id).first()
    message_id = update.message.message_id

    state = user_state.get('state', 0)
    menu_state = user_state.get('menu_state', 0)
    if menu_state == 2 and state==201:
        images_id = user_state.get('images_id', [])
        images_id.append(file_id)
        user_state.update({"images_id": images_id})
        user_log.change_log(user_state)
        
def sort_image(images):
    photo_list = []
    if images and len(images) > 0:
        i = 1
        for image in images:
            if i == 1:
                photo_list.append(InputMediaPhoto(media=image, parse_mode='HTML'))
            else:
                photo_list.append(InputMediaPhoto(media=image))
            i = i + 1
    else:
        pass
    return photo_list

def check_phone_number(phone_number):
        phone_number = phone_number.replace(" ", "")
        if 0 < len(phone_number) < 14:
            if phone_number[0] == '+' and len(phone_number) == 13:
                if phone_number[1:-1].isdigit():
                    return [phone_number, True]
            elif len(phone_number) == 9:
                if phone_number[:-1].isdigit():
                    return [f"+998{phone_number}", True]

            elif len(phone_number) == 12:
                if phone_number[:-1].isdigit():
                    return [f"+{phone_number}", True]
        return False