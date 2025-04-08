# -*- coding: utf-8 -*-
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json


"""VALUE"""


def get_value_one(request, pk):
    value = _query_value_one(pk)
    if value:
        return OrderedDict([
            ('id', value['id']),
            ('label', json.loads(value['label'])),
            ('attribute_id', value.get("attribute_id", None)),
            ('slug', value['slug']),
            ('created_at', value['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('value not found')


def get_value_list(request):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.DASHBOARD_PAGINATE_BY))
    except:
        page = 1
        per_page = settings.DASHBOARD_PAGINATE_BY
    count_records = _query_value_count()
    if request.query_params.get("attribute_id", 0):
        extra_sql = f"WHERE eav_attributevalue.attribute_id = {request.query_params.get('attribute_id', 0)}"
    else:
        extra_sql = ""
    values = _query_value_list(page, per_page, extra_sql)
    items = []
    for data in values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('label', json.loads(data['label'])),
            ('attribute_id', data.get("attribute_id", None)),
            ('slug', data['slug']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_value_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_value.*, eav_attributevalue.attribute_id FROM eav_value
            LEFT JOIN eav_attributevalue ON eav_value.id = eav_attributevalue.value_id WHERE eav_value.id = %s""",
            [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_value_list(page, per_page, extra_sql):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT eav_value.*, eav_attributevalue.attribute_id FROM eav_value 
            LEFT JOIN eav_attributevalue ON eav_value.id = eav_attributevalue.value_id {extra_sql} 
            ORDER BY created_at ASC LIMIT %s OFFSET %s""", [per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_value_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_value""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""ATTRIBUTE VALUE"""


def get_attribute_value_one(request, pk):
    value = _query_attribute_value_one(pk)
    if value:
        return OrderedDict([
            ('id', value['id']),
            ('value', {"label": json.loads(value['value_label'])}),
            ('attribute', {"id": value['attribute_id']}),
            ('sorting', value['sorting']),
            ('created_at', value['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('attribute value not found')


def get_attribute_value_list(request):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.DASHBOARD_PAGINATE_BY))
    except:
        page = 1
        per_page = settings.DASHBOARD_PAGINATE_BY
    if request.query_params.get("attribute_id", 0):
        extra_sql = f"WHERE eav_attributevalue.attribute_id = {request.query_params.get('attribute_id', 0)}"
    else:
        extra_sql = ""
    count_records = _query_attribute_value_count(extra_sql)
    attribute_values = _query_attribute_value_list(page, per_page, extra_sql)
    items = []
    for data in attribute_values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('value', {"label": json.loads(data['value_label'])}),
            ('attribute', {"id": data['attribute_id']}),
            ('sorting', data['sorting']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_attribute_value_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_attributevalue.*, eav_value.label as value_label FROM eav_attributevalue
             INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id WHERE eav_attributevalue.id = %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_attribute_value_list(page, per_page, extra_sql):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT eav_attributevalue.*, eav_value.label as value_label FROM eav_attributevalue
             INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id {extra_sql} ORDER BY slug ASC LIMIT %s OFFSET %s""",
            [per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_attribute_value_count(extra_sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT COUNT(1) as cnt FROM eav_attributevalue
             INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id {extra_sql}""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result
