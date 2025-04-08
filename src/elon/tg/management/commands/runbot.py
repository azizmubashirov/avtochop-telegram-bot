from django.core.management.base import BaseCommand, CommandError
from telegram.ext import (messagequeue as mq, Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler)
from telegram.utils.request import Request
from django.conf import settings
from ...mqbot import MQBot

from elon.tg.views import start, message_handler, photo_handler, callback_handler, contact_handler


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        q = mq.MessageQueue(all_burst_limit=29, all_time_limit_ms=1017)
        request = Request(con_pool_size=36)

        bot = MQBot(settings.BOT_TOKEN, request=request, mqueue=q)
        updater = Updater(bot=bot, use_context=True, workers=32)

        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
        dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))


        updater.start_polling()
        updater.idle()


