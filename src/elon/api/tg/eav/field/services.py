# -*- coding: utf-8 -*-
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json

def get_mark_value_one(request, pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select * from eav_marka
            where eav_marka.id = %s""",[pk]
        )
        rows = dictfetchone(cursor)
    if rows:
        return OrderedDict([
            ('id', rows['id']),
            ('label', json.loads(rows['label'])),
            ('created_at', rows['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('value not found')

def get_model_value_one(request, pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select * from eav_model
                where eav_model.id = %s""",[pk]
        )
        rows = dictfetchone(cursor)
    if rows:
        return OrderedDict([
            ('id', rows['id']),
            ('label', json.loads(rows['label'])),
            ('created_at', rows['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('value not found')

def get_positsion_value_one(request, pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select *  from eav_positsion 
                where eav_positsion.id = %s""",[pk]
        )
        rows = dictfetchone(cursor)
    if rows:
        return OrderedDict([
            ('id', rows['id']),
            ('label', json.loads(rows['label'])),
            ('created_at', rows['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('value not found')
    
def get_marka_category(request, category_marka): 
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))
    except:
        page = 1
        per_page = settings.PER_PAGE
    try:
        search = request.query_params.get('q', '')
    except:
        search = ""
    sql = ""
    if search:
        sql += f" and LOWER(eav_marka.label->>'label_uz') like LOWER('%{search}%') or LOWER(eav_marka.label->>'label_ru') like LOWER('%{search}%')"
    count_records = _query_marka_count(category_marka, sql)
    values = _query_get_marka(category_marka, sql)
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    items = []
    for data in values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('label', json.loads(data['label'])),
            ('image', data['image']),
            ('slug', data['slug']),
            ('sorting', data['sorting']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def _query_get_marka(categry_marka, sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select eav_marka.*  from eav_marka 
                where eav_marka.category = '{categry_marka}' {sql}
                order by sorting"""
        )
        rows = dictfetchall(cursor)
    return rows

def get_model(request, marka_id=None, marka_slug=None):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))
    except:
        page = 1
        per_page = settings.PER_PAGE
    count_records = _query_model_count(marka_id=marka_id, marka_slug=marka_slug)
    values = _query_get_model(marka_id=marka_id, marka_slug=marka_slug)
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    items = []
    for data in values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('label', json.loads(data['label'])),
            ('slug', data['slug']),
            ('sorting', data['sorting']),
            ('parent_id', data['parent_id']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def _query_get_model(marka_id, marka_slug):
    with closing(connection.cursor()) as cursor:
        if marka_id:
            cursor.execute(
                f"""select eav_model.*  from eav_model
                    where eav_model.parent_id = %s
                    order by sorting""", [marka_id]
            )
        elif marka_slug:
            cursor.execute(
                f"""select eav_model.*  from eav_model
                inner join eav_marka em on em.id = eav_model.parent_id 
                where em.slug = %s
                order by eav_model.sorting """, [marka_slug]
            )
        rows = dictfetchall(cursor)
    return rows

def get_positsion(request, model_id=None, model_slug=None):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))
    except:
        page = 1
        per_page = settings.PER_PAGE
    count_records = _query_model_count(model_id, model_slug)

    values = _query_get_positsion(model_id, model_slug)
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    items = []
    for data in values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('label', json.loads(data['label'])),
            ('slug', data['slug']),
            ('parent_id', data['parent_id']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def _query_get_positsion(model_id, model_slug):
    with closing(connection.cursor()) as cursor:
        if model_id:
            cursor.execute(
                f"""select *  from eav_positsion 
                    where eav_positsion.parent_id = %s""", [model_id]
            )
        elif model_slug:
            cursor.execute(
                f"""select eav_positsion.*  from eav_positsion
                    inner join eav_model em on em.id = eav_positsion.parent_id 
                    where em.slug = %s""", [model_slug]
            )
        rows = dictfetchall(cursor)
    return rows

def _query_marka_count(category_marka, sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_marka where eav_marka.category = %s""", [category_marka])
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result

def _query_model_count(marka_id, marka_slug):
    with closing(connection.cursor()) as cursor:
        if marka_id:
            cursor.execute("""SELECT COUNT(1) as cnt FROM eav_model where eav_model.parent_id = %s""", [marka_id])
        elif marka_slug:
            cursor.execute("""SELECT COUNT(1) as cnt FROM eav_model inner join eav_marka em on em.id=eav_model.parent_id  where em.slug = %s""", [marka_slug])
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result
