# -*- coding: utf-8 -*-
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json

def get_category_one(request, pk=None, slug=None):
    category = _query_category_one(pk=pk, slug=slug)
    if category:
        return OrderedDict([
            ('id', category['id']),
            ('title', json.loads(category['title'])),
            ('seo_title', json.loads(category['seo_title'])),
            ('seo_desc', json.loads(category['seo_desc'])),
            ('ads_count', category['ads_count']),
            ('slug', category['slug']),
            ('image', category['image']),
            ('children', category.get('children', [])),
            ('parent', None) if not category['parent_id'] and not category['parent_title'] else ('parent', {"id": category['parent_id'], "title": json.loads(category['parent_title']), 'slug': category['parent_slug']}),
            ('created_at', category['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('category not found')

def get_category_list(request, action="all", category_id=0):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))
    except:
        page = 1
        per_page = settings.PER_PAGE
    count_records = _query_category_count(action, category_id)
    categories = _query_category_list(page, per_page, action, category_id)
    items = []
    for data in categories:
        items.append(OrderedDict([
            ('id', data['id']),
            ('title', json.loads(data['title'])),
            ('seo_title', json.loads(data['seo_title'])),
            ('seo_desc', json.loads(data['seo_desc'])),
            ('ads_count', data['ads_count1']),
            ('slug', data['slug']),
            ('image', data['image']),
            ('children', data.get('children', [])),
            ('parent', {"id": data['parent_id'], "title": json.loads(data['parent_title'])}) if data['parent_id'] and data['parent_title'] else ('parent', None),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S"))
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def _query_category_one(pk=None, slug=None):
    query_param = 't1.id' if pk else 't1.slug'
    query_data = pk if pk else slug
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select t1.*, t3.title as parent_title,t3.slug as parent_slug, (select array_agg(row_to_json(chan)) from (select t2.* from eav_category t2 where t2.parent_id = t1.id)
                 as chan ) as children from eav_category as t1 LEFT JOIN eav_category as t3 ON t1.parent_id = t3.id where {query_param} = %s""", [query_data]
        )

        rows = dictfetchone(cursor)
    return rows

def _query_category_list(page, per_page, action, category_id):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:

        if action == "menu":

            cursor.execute(
                """select t1.*, 
                    (select array_agg(row_to_json(chan)) from 
                        (select t2.*, 
                            (select array_agg(row_to_json(chan2)) from 
                                (select t3.*, t3.ads_count as ads_count1 from 
                                    eav_category t3 where t3.parent_id = t2.id
                                    order by t3.sorting asc
                                ) as chan2
                            ) as children, 
                            case when coalesce((select sum(t3.ads_count) from 
                                eav_category t3 where t3.parent_id = t2.id
                            ), 0) = 0 then t2.ads_count 
                            else (select sum(t3.ads_count) from 
                                eav_category t3 where t3.parent_id = t2.id
                            ) end ads_count1 from 
                            eav_category t2 where t2.parent_id = t1.id order by t2.sorting asc
                        ) as chan 
                    ) as children,
                    (select sum(chan.ads_count1) from 
                        (select 
                            case when coalesce((select sum(t3.ads_count) as ads_count1 from 
                                eav_category t3 where t3.parent_id = t2.id
                            ), 0) = 0 then t2.ads_count 
                            else (select sum(t3.ads_count) as ads_count1 from 
                                eav_category t3 where t3.parent_id = t2.id
                            ) end ads_count1 from eav_category t2 where t2.parent_id = t1.id order by t2.sorting desc
                        ) as chan 
                    )::int as ads_count1
                    from eav_category t1 where t1.parent_id is null order by t1.sorting 
                    LIMIT %s OFFSET %s
                """,[per_page, offset]
            )
        elif action == "sale":
            cursor.execute(
                """select t1.*, 
                        (select array_agg(row_to_json(chan)) from 
                            (select t2.id, t2.title, t2.slug, t2.created_at, t2.parent_id, 
                                (select array_agg(row_to_json(chan2)) from 
                                    (select t3.id, t3.title, t3.slug, t3.created_at, t3.parent_id, t3.ads_count as ads_count1 from 
                                        eav_category t3 where t3.parent_id = t2.id
                                        order by t3.sorting asc
                                    ) as chan2
                                ) as children, 
                                case when coalesce((select sum(t3.ads_count) from 
                                    eav_category t3 where t3.parent_id = t2.id
                                ), 0) = 0 then t2.ads_count 
                                else (select sum(t3.ads_count) from 
                                    eav_category t3 where t3.parent_id = t2.id
                                ) end ads_count1 from 
                                eav_category t2 where t2.parent_id = t1.id order by t2.sorting asc
                            ) as chan 
                        ) as children,
                        (select sum(chan.ads_count1) from 
                            (select 
                                case when coalesce((select sum(t3.ads_count) as ads_count1 from 
                                    eav_category t3 where t3.parent_id = t2.id
                                ), 0) = 0 then t2.ads_count 
                                else (select sum(t3.ads_count) as ads_count1 from 
                                    eav_category t3 where t3.parent_id = t2.id
                                ) end ads_count1 from eav_category t2 where t2.parent_id = t1.id order by t2.sorting desc
                            ) as chan 
                        )::int as ads_count1
                        from eav_category t1 where t1.parent_id is null order by t1.sorting desc
                    LIMIT %s OFFSET %s
                """,[per_page, offset]
            )
        elif action == "children" and category_id:
            part = f"WHERE t1.parent_id = {category_id}"
            cursor.execute(
                f"""SELECT t1.*, t2.title as parent_title FROM eav_category as t1 LEFT JOIN eav_category as t2 
                            ON t1.parent_id = t2.id {part} ORDER BY t1.sorting DESC LIMIT %s OFFSET %s""",
                [per_page, offset]
            )
        else:
            part = ""
            cursor.execute(
                f"""SELECT t1.*, t2.title as parent_title FROM eav_category as t1 LEFT JOIN eav_category as t2 
                ON t1.parent_id = t2.id {part} ORDER BY t1.sorting DESC"""
            )
        rows = dictfetchall(cursor)
    return rows

def _query_category_count(action, category_id):
    with closing(connection.cursor()) as cursor:
        if action == "menu":
            part = "WHERE parent_id is NULL"
        elif action == "children" and category_id:
            part = f"WHERE parent_id = {category_id}"
        else:
            part = ""
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM eav_category {part}""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result

def get_category_steps(request, category_id, next_page=None, per_page_count=None):
    try:
        page = int(request.query_params.get('page', 1))
        per_page =  int(request.query_params.get('per_page'))
    except:
        page = next_page if next_page else 1
        per_page = per_page_count if per_page_count else 1

    steps = _query_category_steps(category_id)
    field_ids = []
    step_items = []
    entity_id = 0
    for data in steps:
        field_ids += list(data['children'])
        entity_id = int(data['id'])
        step_items.append(OrderedDict([
            ('id', data['id']),
            ('title', json.loads(data['title'])),
            ('config', json.loads(data['config'])),
            ('children', [{"id": child} for child in data['children']]),
            ('slug', data['slug']),
        ]))
    if field_ids:
        fields = _query_category_fields(field_ids, entity_id, page, per_page)
        fields_count = _query_category_field_count(field_ids, entity_id)
    else:
        fields = _query_category_fields([], entity_id, page, per_page)
        fields_count = _query_category_field_count([], entity_id)
    
    step_fields = []
    for data in fields:
        step_fields.append(OrderedDict([
            ('id', data['id']),
            ('properties', json.loads(data['properties'])),
            ('is_price', data['is_price']),
            ('price_state', data['price_state']),
            ('input_type', data['input_type']),
            ('values', json.loads(data['values']) if data['values'] else None),
            ('parent', {"id": data['parent_id']} if data['parent_id'] else None),
            ('slug', data['slug']),
        ]))
    if request:
        paginator = SqlPaginator(request, page=page, per_page=per_page, count=fields_count.get('count'))
        paging = paginator.get_paginated_response()
        return OrderedDict([
            ('steps', step_items),
            ('fields', step_fields),
            ('meta', paging)
        ])
    else:
        return OrderedDict([
            ('steps', step_items),
            ('fields', step_fields)
        ])

def _query_category_steps(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
                """WITH table1 AS (SELECT eav_entity.* FROM eav_categoryentity INNER JOIN eav_entity 
                    ON eav_categoryentity.entity_id = eav_entity.id WHERE category_id = %s ORDER BY eav_categoryentity.sorting)
                    SELECT t.*, ARRAY(SELECT eav_entityattribute.attribute_id FROM eav_entityattribute WHERE eav_entityattribute.entity_id = t.id ORDER BY eav_entityattribute.sorting)
                    AS children FROM table1 t
                """, [category_id]
        )
        rows = dictfetchall(cursor)
    return rows

def _query_category_fields(fields, entity_id, page, per_page):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """WITH table1 AS (SELECT eav_attribute.*, eav_inputtype.title AS input_type FROM eav_entityattribute
            inner join eav_attribute on eav_entityattribute.attribute_id = eav_attribute.id
            INNER JOIN eav_inputtype ON eav_attribute.input_type_id = eav_inputtype.id
            WHERE eav_attribute.id IN ({}) and eav_entityattribute.entity_id = {}
            order by eav_entityattribute.sorting )
            SELECT t.*, (SELECT JSONB_AGG(v) FROM (SELECT eav_value.id, eav_value."label", eav_value.parent_id, eav_value.image FROM eav_attributevalue 
            INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id WHERE 
            eav_attributevalue.attribute_id = t.id order by eav_attributevalue.sorting) v) AS "values" FROM table1 t limit {} offset {}""".format(str(fields).strip("[]"), entity_id, per_page, offset)
        )
        rows = dictfetchall(cursor)
    return rows

def _query_category_field_count(fields, entity_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """WITH table1 AS (SELECT eav_attribute.*, eav_inputtype.title AS input_type FROM eav_entityattribute
                    inner join eav_attribute on eav_entityattribute.attribute_id = eav_attribute.id
                    INNER JOIN eav_inputtype ON eav_attribute.input_type_id = eav_inputtype.id
                    WHERE eav_attribute.id IN ({}) and eav_entityattribute.entity_id = {}
                    order by eav_entityattribute.sorting )
                    SELECT count(1)  FROM table1 t """.format(str(fields).strip("[]"), entity_id)
                )
        rows = dictfetchone(cursor)
    return rows