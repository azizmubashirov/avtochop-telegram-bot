# -*- coding: utf-8 -*-
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from django.conf import settings
from eelon.base.utils.db import dictfetchone, dictfetchall
from eelon.base.utils.sqlpaginator import SqlPaginator
import json


PER_PAGE = settings.PAGINATE_BY


def list_product(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * PER_PAGE

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT users_user.* FROM users_user WHERE is_active is true ORDER BY user_id DESC LIMIT %s OFFSET %s""",
            [PER_PAGE, offset]
        )
        items = dictfetchall(cursor)
        result = []
        for data in items:
            result.append(_format(data))

    with closing(connection.cursor()) as cursor:
        cursor.execute(
            "SELECT COUNT(1) AS cnt FROM users_users WHERE is_active IS true")
        row = dictfetchone(cursor)

    if row:
        count_records = row['cnt']
    else:
        count_records = 0

    paginator = SqlPaginator(request, page=1, per_page=PER_PAGE, count=count_records)
    pagging = paginator.get_paginated_response()

    return OrderedDict([
        ('items', result),
        ('meta', pagging)
    ])


def one_user_by_pk(request, pk=0):
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute("""SELECT users_user.* FROM users_user WHERE id = %s AND is_active IS true""", [pk])
            data = dictfetchone(cursor)
            if data:
                result = _format(data)
            else:
                result = None
        return result
    except Exception as e:
        print("Error during fetching user by pk in services.py:", e)


def one_user_by_chat_id(request, chat_id=None):
    try:
        with closing(connection.cursor()) as cursor:
            cursor.execute("""SELECT users_user.* FROM users_user WHERE chat_id = %s AND is_active IS true""", [chat_id])
            data = dictfetchone(cursor)
            if data:
                result = _format(data)
            else:
                result = None
        return result
    except Exception as e:
        print("Error during fetching user by hcat_id in services.py:", e)


def _format(data):
    return OrderedDict([
        ('id', data['id']),
        ('email', data['email']),
        ('phone_number', data['phone_number']),
        ('nickname', data['nickname']),
        ('firstname', data['firstname']),
        ('lastname', data['lastname']),

        ('chat_id', data['chat_id']),
        ('tg_username', data['tg_username']),
        ('tg_firstname', data['tg_firstname']),
        ('tg_lastname', data['tg_lastname']),
        ('is_telegram', data['is_telegram']),

        ('tab_number', data['tab_number']),
        ('image', data['image']),
        ('date_joined', data['date_joined']),
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

