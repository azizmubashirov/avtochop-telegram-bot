# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from elon.base.utils.db import dictfetchone, dictfetchall
import json


def list_product(request):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT users_user.* FROM users_user WHERE is_active is true ORDER BY users_user.id DESC """,
        )
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT COUNT(1) AS cnt FROM users_user WHERE users_user.is_active IS true")
        row = dictfetchone(cursor)

    return OrderedDict([
        ('data', result)
    ])

def list_search(request):
    search = request.GET.get("search", "")
    page = request.GET.get('page', 1)
    limit = 30
    offset = (int(page) - 1) * limit
    results = []
    if search:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """SELECT users_user.* FROM users_user WHERE (
                email like '%{}%' or phone_number like '%{}%' or 
                nickname like '%{}%' or chat_id::varchar like '%{}%' or 
                tg_username like '%{}%') and is_active is true
                ORDER BY id desc limit {} offset {}""".format(
                    search, search, search, search, search, limit, offset
                )
            )
            items = dictfetchall(cursor)
            for data in items:
                temp = {
                    "id": data['id'],
                    "is_telegram": data['is_telegram'],
                    "chat_id": data['chat_id'],
                    "tg_username": data['tg_username'],
                    "email": data['email'],
                    "phone_number": data['phone_number'],
                    "nickname": data['nickname'],
                    "tg_firstname": data['tg_firstname'],
                    "tg_lastname": data['tg_lastname'],
                }
                if data['is_telegram']:
                    text = "{" + f""""id": {data['id']}, "is_telegram": 1, "chat_id": {data['chat_id']}, "tg_username": "{data['tg_username']}", "tg_firstname": "{data['tg_firstname']}", "tg_lastname": "{data['tg_lastname']}", "phone_number": "{data['phone_number']}\"""" + "}"
                else:
                    text = "{" + f""""id": {data['id']}, "is_telegram": 0, "email": "{data['email']}", "phone_number": "{data['phone_number']}", "nickname": "{data['nickname']}\"""" + "}"
                temp['text'] = text
                results.append(temp)
    res = {
        "results": results,
        "pagination": {
            "more": True
        }
    }
    return res


def _format(data):
    return OrderedDict([
        ('id', data['id']),
        ('email', data['email']),
        ('phone_number', data['phone_number']),
        ('firstname', data['tg_firstname']),
        ('lastname', data['tg_lastname']),
        ('tab_number', data['tab_number']),
        ('image', data['image']),
        ('chat_id', data['chat_id']),
        ('date_joined', data['date_joined'].strftime("%Y-%m-%d %H:%M:%S")),
    ])


def one_log(request, user_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT user_id, messages FROM users_log WHERE user_id = %s""", [user_id])
        data = dictfetchone(cursor)
        if data:
            result = _log_format(data)
        else:
            result = None
    return result


def _log_format(data):
    return OrderedDict([
        ('user_id', data['user_id']),
        ('messages', json.loads(data['messages'])),
    ])


