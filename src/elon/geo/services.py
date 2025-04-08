# -*- coding: utf-8 -*-
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json

PER_PAGE = settings.PER_PAGE


def get_region_one(request, pk):
    category = _query_region_one(pk)
    if category:
        return OrderedDict([
            ('id', category['id']),
            ('name_uz', category['name_uz']),
            ('name_ru', category['name_ru']),
            ('ordering', category['ordering']),
        ])
    else:
        raise NotFound('Region not found')


def get_region_with_children(request, pk):
    category = _query_region_with_children(pk)
    if category:
        return OrderedDict([
            ('id', category['id']),
            ('name_uz', category['name_uz']),
            ('name_ru', category['name_ru']),
            ('ordering', category['ordering']),
            ('children', json.loads(category['children'])),
        ])
    else:
        raise NotFound('category not found')


def get_region_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    search = request.query_params.get('q', '')
    sql = ""
    if search:
        sql += f"where LOWER(geo_region.name_uz) like LOWER('%{search}%') or LOWER(geo_region.name_ru) like LOWER('%{search}%')"
    count_records = _query_region_count(sql)
    categories = _query_region_list(page, sql)
    items = []
    for data in categories:
        items.append(OrderedDict([
            ('id', data['id']),
            ('name_uz', data['name_uz']),
            ('name_ru', data['name_ru']),
            ('ordering', data['ordering']),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_region_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT * FROM geo_region WHERE id = %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_region_with_children(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT *, (SELECT JSONB_AGG(gd) FROM (SELECT * FROM geo_district 
            WHERE geo_district.region_id = geo_region.id) gd) AS children 
            FROM geo_region WHERE geo_region.id = %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_region_list(page, sql):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT * FROM geo_region {sql} ORDER BY ordering ASC"""
        )
        rows = dictfetchall(cursor)
    return rows


def _query_region_count(sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM geo_region {sql}""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""------------------------------------------------------------------------------------------------------------------"""


def get_district_one(request, pk):
    category = _query_district_one(pk)
    if category:
        return OrderedDict([
            ('id', category['id']),
            ('name_uz', category['name_uz']),
            ('name_ru', category['name_ru']),
            ('ordering', category['ordering']),
            ('region', category['region']),
        ])
    else:
        raise NotFound('District not found')


def get_district_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_district_count()
    categories = _query_district_list(page)
    items = []
    for data in categories:
        items.append(OrderedDict([
            ('id', data['id']),
            ('name_uz', data['name_uz']),
            ('name_ru', data['name_ru']),
            ('ordering', data['ordering']),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_district_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT geo_district.*, row_to_json(geo_region) as region
            FROM geo_district LEFT JOIN geo_region ON geo_district.region_id = geo_region.id 
            WHERE geo_district.id =  %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_district_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT * FROM geo_district ORDER BY ordering ASC LIMIT %s OFFSET %s""", [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_district_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM geo_district""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result
