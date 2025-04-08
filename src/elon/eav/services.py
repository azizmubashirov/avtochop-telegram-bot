# -*- coding: utf-8 -*-
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from eelon.base.utils.db import dictfetchall, dictfetchone
from eelon.base.utils.sqlpaginator import SqlPaginator
import json

PER_PAGE = settings.DASHBOARD_PAGINATE_BY


"""CATEGORY"""


def get_category_one(request, pk):
    category = _query_category_one(pk)
    if category:
        return OrderedDict([
            ('id', category['id']),
            ('title', json.loads(category['title'])),
            ('slug', category['slug']),
            ('parent', None) if not category['parent_id'] and not category['parent_title'] else ('parent', {"id": category['parent_id'], "title": json.loads(category['parent_title'])}),
            ('created_at', category['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('category not found')


def get_category_list(request, action="all", category_id=0):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_category_count()
    categories = _query_category_list(page, action, category_id)
    items = []
    for data in categories:
        items.append(OrderedDict([
            ('id', data['id']),
            ('title', json.loads(data['title'])),
            ('slug', data['slug']),
            ('parent', None) if not data['parent_id'] and not data['parent_title'] else ('parent', {"id": data['parent_id'], "title": json.loads(data['parent_title'])}),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_category_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT t1.*, t2.title as parent_title FROM eav_category as t1 
            LEFT JOIN eav_category as t2 ON t1.parent_id = t2.id WHERE t1.id = %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_category_list(page, action, category_id):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:

        if action == "menu":
            part = "WHERE t1.parent_id is NULL"
        elif action == "children" and category_id:
            part = f"WHERE t1.parent_id = {category_id}"
        else:
            part = ""

        cursor.execute(
            f"""SELECT t1.*, t2.title as parent_title FROM eav_category as t1 LEFT JOIN eav_category as t2 
            ON t1.parent_id = t2.id {part} ORDER BY t1.sorting ASC LIMIT %s OFFSET %s""", [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_category_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_category""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""INPUT TYPE"""


def get_input_type_one(request, pk):
    input_type = _query_input_type_one(pk)
    if input_type:
        return OrderedDict([
            ('id', input_type['id']),
            ('title', input_type['title']),
            ('slug', input_type['slug']),
            ('created_at', input_type['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('input type not found')


def get_input_type_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_input_type_count()
    input_types = _query_input_type_list(page)
    items = []
    for data in input_types:
        items.append(OrderedDict([
            ('id', data['id']),
            ('title', data['title']),
            ('slug', data['slug']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_input_type_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT * FROM eav_inputtype WHERE id = %s""", [pk])
        rows = dictfetchone(cursor)
    return rows


def _query_input_type_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT * FROM eav_inputtype ORDER BY slug ASC LIMIT %s OFFSET %s""", [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_input_type_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_inputtype""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""ENTITY"""


def get_entity_one(request, pk):
    entity = _query_entity_one(pk)
    if entity:
        return OrderedDict([
            ('id', entity['id']),
            ('title', json.loads(entity['title'])),
            ('slug', entity['slug']),
            ('sorting', entity['sorting']),
            ('config', json.loads(entity['config'])),
            ('created_at', entity['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('entity not found')


def get_entity_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_entity_count()
    entities = _query_entity_list(page)
    items = []
    for data in entities:
        items.append(OrderedDict([
            ('id', data['id']),
            ('title', json.loads(data['title'])),
            ('slug', data['slug']),
            ('sorting', data['sorting']),
            ('config', json.loads(data['config'])),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_entity_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT * FROM eav_entity WHERE id = %s""", [pk])
        rows = dictfetchone(cursor)
    return rows


def _query_entity_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT * FROM eav_entity ORDER BY slug ASC LIMIT %s OFFSET %s""", [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_entity_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_entity""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""CATEGORY ENTITY"""


def get_category_entity_one(request, pk):
    entity = _query_category_entity_one(pk)
    if entity:
        return OrderedDict([
            ('id', entity['id']),
            ('category', {"id": entity['category_id'], "title": json.loads(entity['category_title'])}),
            ('entity', {"id": entity['entity_id'], "title": json.loads(entity['entity_title'])}),
            ('sorting', entity['sorting']),
            ('created_at', entity['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('category entity not found')


def get_category_entity_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_category_entity_count()
    entities = _query_category_entity_list(page)
    items = []
    for data in entities:
        items.append(OrderedDict([
            ('id', data['id']),
            ('category', {"id": data['category_id'], "title": json.loads(data['category_title'])}),
            ('entity', {"id": data['entity_id'], "title": json.loads(data['entity_title'])}),
            ('sorting', data['sorting']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_category_entity_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_categoryentity.*, eav_category.title as category_title,  eav_entity.title as entity_title FROM eav_categoryentity 
            INNER JOIN eav_category ON eav_categoryentity.category_id = eav_category.id 
            INNER JOIN eav_entity ON eav_categoryentity.entity_id = eav_entity.id WHERE eav_categoryentity.id = %s""", [pk])
        rows = dictfetchone(cursor)
    return rows


def _query_category_entity_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_categoryentity.*, eav_category.title as category_title,  eav_entity.title as entity_title FROM eav_categoryentity 
            INNER JOIN eav_category ON eav_categoryentity.category_id = eav_category.id 
            INNER JOIN eav_entity ON eav_categoryentity.entity_id = eav_entity.id ORDER BY eav_categoryentity.sorting ASC LIMIT %s OFFSET %s""",
            [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_category_entity_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_entity""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""ATTRIBUTE"""


def get_attribute_one(request, pk):
    attribute = _query_attribute_one(pk)
    if attribute:
        return OrderedDict([
            ('id', attribute['id']),
            ('input_type', {"id": attribute['input_type_id'], "title": attribute['input_type_title']}),
            ('parent', {"id": attribute['parent_id']} if attribute['parent_id'] else None),
            ('slug', attribute['slug']),
            ('properties', json.loads(attribute['properties'])),
            ('created_at', attribute['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('attribute not found')


def get_attribute_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_attribute_count()
    attributes = _query_attribute_list(page)
    items = []
    for data in attributes:
        items.append(OrderedDict([
            ('id', data['id']),
            ('input_type', {"id": data['input_type_id'], "title": data['input_type_title']}),
            ('slug', data['slug']),
            ('parent', {"id": data['parent_id']} if data['parent_id'] else None),
            ('properties', json.loads(data['properties'])),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_attribute_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_attribute.*, eav_inputtype.title as input_type_title FROM eav_attribute LEFT JOIN eav_inputtype
             ON eav_attribute.input_type_id = eav_inputtype.id WHERE eav_attribute.id = %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_attribute_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_attribute.*, eav_inputtype.title as input_type_title FROM eav_attribute LEFT JOIN eav_inputtype
             ON eav_attribute.input_type_id = eav_inputtype.id ORDER BY eav_attribute.slug ASC LIMIT %s OFFSET %s""",
            [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_attribute_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM eav_attribute""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""ENTITY ATTRIBUTE"""


def get_entity_attribute_one(request, pk):
    entity_attribute = _query_entity_attribute_one(pk)
    if entity_attribute:
        return OrderedDict([
            ('id', entity_attribute['id']),
            ('attribute', {"id": entity_attribute['attribute_id']}),
            ('entity', {"id": entity_attribute['entity_id'], "title": json.loads(entity_attribute['entity_title'])}),
            ('sorting', entity_attribute['sorting']),
            ('created_at', entity_attribute['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('entity attribute not found')


def get_entity_attribute_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_entity_attribute_count()
    entity_attributes = _query_entity_attribute_list(page)
    items = []
    for data in entity_attributes:
        items.append(OrderedDict([
            ('id', data['id']),
            ('attribute', {"id": data['attribute_id']}),
            ('entity', {"id": data['entity_id'], "title": json.loads(data['entity_title'])}),
            ('sorting', data['sorting']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_entity_attribute_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_entityattribute.*, eav_entity.title as entity_title, eav_attribute.id as attribute_id FROM eav_entityattribute
            INNER JOIN eav_entity ON eav_entityattribute.entity_id = eav_entity.id
            INNER JOIN eav_attribute ON eav_entityattribute.attribute_id = eav_attribute.id
            WHERE eav_entityattribute.id = %s""", [pk])
        rows = dictfetchone(cursor)
    return rows


def _query_entity_attribute_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_entityattribute.*, eav_entity.title as entity_title, eav_attribute.id as attribute_id FROM eav_entityattribute
            INNER JOIN eav_entity ON eav_entityattribute.entity_id = eav_entity.id
            INNER JOIN eav_attribute ON eav_entityattribute.attribute_id = eav_attribute.id ORDER BY eav_entityattribute.sorting ASC LIMIT %s OFFSET %s""", [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_entity_attribute_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM (SELECT eav_entityattribute.*, eav_entity.title as entity_title, eav_attribute.id as attribute_id FROM eav_entityattribute
            INNER JOIN eav_entity ON eav_entityattribute.entity_id = eav_entity.id
            INNER JOIN eav_attribute ON eav_entityattribute.attribute_id = eav_attribute.id) as t1""")
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""VALUE"""


def get_value_one(request, pk):
    value = _query_value_one(pk)
    if value:
        return OrderedDict([
            ('id', value['id']),
            ('label', json.loads(value['label'])),
            ('slug', value['slug']),
            ('created_at', value['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('value not found')


def get_value_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1
    count_records = _query_value_count()
    values = _query_value_list(page)
    items = []
    for data in values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('label', json.loads(data['label'])),
            ('slug', data['slug']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_value_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT * FROM eav_value WHERE id = %s""", [pk]
        )
        rows = dictfetchone(cursor)
    return rows


def _query_value_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT * FROM eav_value ORDER BY slug ASC LIMIT %s OFFSET %s""", [PER_PAGE, offset]
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
    except:
        page = 1
    count_records = _query_value_count()
    attribute_values = _query_attribute_value_list(page)
    items = []
    for data in attribute_values:
        items.append(OrderedDict([
            ('id', data['id']),
            ('value', {"label": json.loads(data['value_label'])}),
            ('attribute', {"id": data['attribute_id']}),
            ('sorting', data['sorting']),
            ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
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


def _query_attribute_value_list(page):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_attributevalue.*, eav_value.label as value_label FROM eav_attributevalue
             INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id ORDER BY slug ASC LIMIT %s OFFSET %s""",
            [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_attribute_value_count():
    with closing(connection.cursor()) as cursor:
        cursor.execute("""SELECT COUNT(1) as cnt FROM (SELECT eav_attributevalue.*, eav_value.label as value_label FROM eav_attributevalue
             INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id) """)
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


""""""


def get_category_steps(request, category_id):
    steps = _query_category_steps(category_id)
    field_ids = []
    step_items = []
    for data in steps:
        field_ids += list(data['children'])
        step_items.append(OrderedDict([
            ('id', data['id']),
            ('title', json.loads(data['title'])),
            ('config', json.loads(data['config'])),
            ('children', [{"id": child} for child in data['children']]),
            ('slug', data['slug']),
            # ('sorting', data['sorting']),
            # ('created_at', data['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))

    fields = _query_category_fields(field_ids) if field_ids else []
    step_fields = []
    for data in fields:
        step_fields.append(OrderedDict([
            ('id', data['id']),
            ('properties', json.loads(data['properties'])),
            ('input_type', data['input_type']),
            ('values', json.loads(data['values']) if data['values'] else None),
            ('parent', {"id": data['parent_id']} if data['parent_id'] else None),
            ('slug', data['slug']),
        ]))

    return OrderedDict([
        ('steps', step_items),
        ('fields', step_fields)
    ])


def _query_category_steps(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """WITH table1 AS (SELECT eav_entity.* FROM eav_categoryentity INNER JOIN eav_entity 
            ON eav_categoryentity.entity_id = eav_entity.id WHERE category_id = %s ORDER BY eav_categoryentity.sorting)
            SELECT t.*, ARRAY(SELECT eav_entityattribute.attribute_id FROM eav_entityattribute WHERE eav_entityattribute.entity_id = t.id)
            AS children FROM table1 t""", [category_id]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_category_fields(fields):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """WITH table1 AS (SELECT eav_attribute.*, eav_inputtype.title AS input_type FROM eav_attribute INNER JOIN 
            eav_inputtype ON eav_attribute.input_type_id = eav_inputtype.id WHERE eav_attribute.id IN ({}))
            SELECT t.*, (SELECT JSONB_AGG(v) FROM (SELECT eav_value.id, eav_value."label", eav_value.parent_id FROM eav_attributevalue 
            INNER JOIN eav_value ON eav_attributevalue.value_id = eav_value.id WHERE 
            eav_attributevalue.attribute_id = t.id) v) AS "values" FROM table1 t""".format(str(fields).strip("[]"))
        )
        rows = dictfetchall(cursor)
    return rows
