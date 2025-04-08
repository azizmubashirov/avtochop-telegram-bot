from telegram import ReplyMarkup, bot, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, \
    ReplyKeyboardRemove, InputMediaPhoto, BotCommand, WebAppInfo

from elon.users.models import User, Temp
from elon.tg.userdata import UserLog
from elon.tg.sends import *
import re
import random
import string

BUTTON = {
    "ads_create":{
        1: "E'lon qo'shish",
        2: "Oбъявления cоздать"
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
class RegisterView(UserLog):
    def __init__(self, user_data):
        super().__init__(user_data)

    def message_handler(self, context, update, text, user_data):
        user_state = self.get_log()
        state = user_state.get('state', 100)

        if state == 100:
            user_state.update({'state': 102})
            self.change_log(user_state)
            text = "Raqamni yuborish 📞" if user_state.get('lang_id') == 1 else "Отправить номер 📞"
            contact_number = KeyboardButton(text=text, request_contact=True)
            go_message(context=context,
                       message="Iltimos <b>Raqamni yuborish</b> tugmasini bosib raqamni yuboring yoki qo'lda yozib yuboring" if user_state.get('lang_id') == 1 else "Отправьте номер, нажав кнопку <b>Отправить номер</b>, или отправьте его вручную.",
                       user_id=user_data.id,
                       reply_markup=ReplyKeyboardMarkup([[contact_number]], resize_keyboard=True
                       ))
            return 1
        elif state == 102:
            phone_number = self.check_phone_number(text)
            if phone_number and phone_number[1]:
                user = User.objects.filter(phone_number=phone_number[0]).first()
                if not user:
                    user_state.update({'state': 103})
                    sms_code = ''.join(random.choice(string.digits) for _ in range(4))
                    user_state['contact'] = {'phone_number': phone_number[0], 'code': sms_code}
                    print(sms_code)
                    self.change_log(user_state)
                    message = f"<b>Tasdiqlash kodini kiriting:</b> {sms_code}" if user_state.get('lang_id') == 1 else f"<b>Введите проверочный код 👇</b> {sms_code}"
                    go_message(context=context, user_id=user_data.id, message=message)
                else:
                    message = f"<b>❌ Xato</b>\n\n Bu telefon raqam oldin ro'yxatan o'tgan" if user_state.get('lang_id') == 1 else f"<b>❌ Ошибка</b>\n\n Этот номер телефона уже зарегистрирован"
                    go_message(context, user_id=user_data.id, message=message)
            else:
                message = f"<b>❌ Xato</b>\n\n Telefon raqamingizni to'g'ri kiriting!" if user_state.get('lang_id') == 1 else f"<b>❌ Ошибка</b>\n\n Введите свой номер телефона правильно!"
                go_message(context, user_id=user_data.id, message=message)

        elif state == 103:
            if user_state.get('contact').get("code") == text:
                user = User(
                    chat_id=user_data.id,
                    tg_username=user_data.username,
                    tg_firstname=user_data.first_name,
                    tg_lastname=user_data.last_name,
                    phone_number = user_state.get('contact').get('phone_number'),
                    email = user_state.get('contact').get('phone_number'),
                    is_telegram=True,
                    is_verified = True,
                    is_staff = True
                )
                user.set_password(text)
                user.save()
                Temp(
                    firstname=user_data.first_name, 
                    lastname=user_data.last_name,
                    phone_number=user_state.get('contact').get('phone_number'),
                    verified = True,
                    verified_code = text
                ).save()
                self.menu(user_data.id, user_state.get('lang_id'), context)
                return 1
            else:
                message = f"<b>❌ Xato</b>\n\n kodni togri kiriting!" if user_state.get('lang_id') == 1 else f"<b>❌ Ошибка</b>\n\n введите код правильно!"
                go_message(context, user_id=user_data.id, message=message)

    def menu(user_id, lang, context):
        user = User.objects.filter(chat_id=user_id).first()
        ads_create = WebAppInfo(f"") 
        ads_view = WebAppInfo(f"") 
        favourite_ads = WebAppInfo(f"") 
        my_ads = WebAppInfo(f"") 
        button = [
            [KeyboardButton(BUTTON['ads_create'][lang], web_app=ads_create), KeyboardButton(BUTTON['ads_view'][lang], web_app=ads_view)],
            [KeyboardButton(BUTTON['favourite_ads'][lang], web_app=favourite_ads), KeyboardButton(BUTTON['my_ads'][lang], web_app=my_ads)]
        ]
        message = "<b></b> ga xush kelibsiz!\n\n<b>Kerakli bo‘limni tanlang:</b>👇" if lang == 1 else "Добро пожаловать в <b>Avtopik</b>!\n\n<b>Выберите нужный раздел:</b>👇"
        go_message(context=context, user_id=user_id, message=message,
                reply_markup=ReplyKeyboardMarkup(button, one_time_keyboard=False, resize_keyboard=True))

    def check_phone_number(self, phone_number):
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