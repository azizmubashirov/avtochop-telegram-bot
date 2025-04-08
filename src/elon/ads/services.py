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


def get_ad_one(request, pk):
    ad = _query_ad_one(pk)
    if ad:
        return OrderedDict([
            ('id', ad['id']),
            ('title', ad['title']),
            ('description', ad['description']),
            ('images', ad['images']),
            ('price', ad['price']),
            ('description', ad['description']),
            ('properties', json.loads(ad['properties'])),
            ('fields', ad['fields']),
            ('user_id', ad['user_id'] if ad['user_id'] else None),
            ('contact', json.loads(ad['contact'])),
            ('location', json.loads(ad['location'])),
            ('category', None) if not ad['category_id'] and not ad['category_title'] else ('category', {"id": ad['category_id'], "title": json.loads(ad['category_title'])}),
            ('region', None) if not ad['region_id'] else ('region', {"id": ad['region_id'],
                                                                     "name": {"name_uz": ad['region_name_uz'],
                                                                              "name_ru": ad['region_name_ru']}}),
            ('district', None) if not ad['district_id'] else ('district', {"id": ad['district_id'],
                                                                           "name": {"name_uz": ad['district_name_uz'],
                                                                                    "name_ru": ad[
                                                                                        'district_name_ru']}}),
            ('created_at', ad['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ])
    else:
        raise NotFound('ad not found')


def get_ad_list(request):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    ad_type = request.query_params.get('ad_type', 0)
    category_id = request.query_params.get('category', 0)
    region_id = request.query_params.get('region', 0)
    district_id = request.query_params.get('district', 0)
    user_id = request.query_params.get('user', 0)
    web_user_id = request.query_params.get('web_user', 0)

    extra_sql = "where "
    sql = ""

    if ad_type or category_id or region_id or district_id or user_id or web_user_id:
        sql = extra_sql

    if user_id:
        sql += f"users_user.chat_id = {user_id} and "

    elif web_user_id:
        sql += f"ads_ad.user_id = {web_user_id} and "

    if ad_type:
        sql += f"ads_ad.ad_type = {ad_type} and "

    if category_id:
        sql += f"ads_ad.category_id = {category_id} and "

    if region_id:
        sql += f"ads_ad.region_id = {region_id} and "

    if district_id:
        sql += f"ads_ad.district_id = {district_id} and "

    sql = sql.strip("and ")
    count_records = _query_ads_count(sql)
    ads = _query_ads_list(page, sql)
    items = []
    for ad in ads:
        items.append(OrderedDict([
            ('id', ad['id']),
            ('title', ad['title']),
            ('description', ad['description']),
            ('images', ad['images']),
            ('price', ad['price']),
            ('description', ad['description']),
            ('properties', json.loads(ad['properties']) if ad['properties'] else None),
            ('fields', ad['fields']),
            ('user_id', ad['user_id'] if ad['user_id'] else None),
            ('contact', json.loads(ad['contact'])),
            ('location', json.loads(ad['location'])),
            ('category', None) if not ad['category_id'] and not ad['category_title'] else ('category', {"id": ad['category_id'], "title": json.loads(ad['category_title'])}),
            ('region', None) if not ad['region_id'] else ('region', {"id": ad['region_id'], "name": {"name_uz": ad['region_name_uz'], "name_ru": ad['region_name_ru']}}),
            ('district', None) if not ad['district_id'] else ('district', {"id": ad['district_id'], "name": {"name_uz": ad['district_name_uz'], "name_ru": ad['district_name_ru']}}),
            ('created_at', ad['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def get_ad_list_by_categories(request, categories):
    try:
        page = int(request.query_params.get('page', 1))
    except:
        page = 1

    count_records = _query_ads_count_by_categories(categories)
    ads = _query_ads_list_by_categories(page, categories)
    items = []

    for ad in ads:
        items.append(OrderedDict([
            ('id', ad['id']),
            ('title', ad['title']),
            ('description', ad['description']),
            ('images', ad['images']),
            ('price', ad['price']),
            ('description', ad['description']),
            ('properties', json.loads(ad['properties'])),
            ('fields', ad['fields']),
            ('user_id', ad['user_id'] if ad['user_id'] else None),
            ('contact', json.loads(ad['contact'])),
            ('location', json.loads(ad['location'])),
            ('category', None) if not ad['category_id'] and not ad['category_title'] else (
            'category', {"id": ad['category_id'], "title": json.loads(ad['category_title'])}),
            ('region', None) if not ad['region_id'] else ('region', {"id": ad['region_id'],
                                                                     "name": {"name_uz": ad['region_name_uz'],
                                                                              "name_ru": ad['region_name_ru']}}),
            ('district', None) if not ad['district_id'] else ('district', {"id": ad['district_id'],
                                                                           "name": {"name_uz": ad['district_name_uz'],
                                                                                    "name_ru": ad[
                                                                                        'district_name_ru']}}),
            ('created_at', ad['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=PER_PAGE, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_ad_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select ads_ad.*
            ,eav_category.title as category_title 
            ,geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru
            ,geo_region.name_uz as region_name_uz, geo_region.name_ru as region_name_ru 
            , (select array_agg(row_to_json(qaz)) from (
            select eav_attribute.id, eav_attribute.properties->>'label' as "label", eav_attribute.slug, 
            case when eav_value."label" is not null then eav_value."label" 
            else jsonb_build_object('label', jsonb_build_object('label_uz', ads_ad.properties->>eav_attribute.slug, 'label_ru', ads_ad.properties->>eav_attribute.slug)) 
            end as value_label
            from eav_attribute 
            left join eav_attributevalue on eav_attribute.id = eav_attributevalue.attribute_id
            left join eav_value on eav_attributevalue.value_id = eav_value.id
            left join eav_inputtype on eav_attribute.input_type_id = eav_inputtype.id
            where (eav_value.id::text = ads_ad.properties->>eav_attribute.slug or eav_value."label" is null) and eav_attribute.slug in (select jsonb_object_keys(ads_ad.properties))) qaz) as fields
            from ads_ad
            inner join eav_category on ads_ad.category_id = eav_category.id
            left join geo_district on ads_ad.district_id = geo_district.id
            left join geo_region on ads_ad.region_id = geo_region.id
            where ads_ad.id = %s""", [int(pk)]
        )
        row = dictfetchone(cursor)
    return row


def _query_ads_list(page, sql):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select ads_ad.*
            ,eav_category.title as category_title 
            ,geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru
            ,geo_region.name_uz as region_name_uz, geo_region.name_ru as region_name_ru 
            , (select array_agg(row_to_json(qaz)) from (
            select eav_attribute.id, eav_attribute.properties->>'label' as "label", eav_attribute.slug, 
            case when eav_value."label" is not null then eav_value."label" 
            else jsonb_build_object('label', jsonb_build_object('label_uz', ads_ad.properties->>eav_attribute.slug, 'label_ru', ads_ad.properties->>eav_attribute.slug)) 
            end as value_label
            from eav_attribute 
            left join eav_attributevalue on eav_attribute.id = eav_attributevalue.attribute_id
            left join eav_value on eav_attributevalue.value_id = eav_value.id
            left join eav_inputtype on eav_attribute.input_type_id = eav_inputtype.id
            where (eav_value.id::text = ads_ad.properties->>eav_attribute.slug or eav_value."label" is null) and eav_attribute.slug in (select jsonb_object_keys(ads_ad.properties))) qaz) as fields
            from ads_ad
            inner join eav_category on ads_ad.category_id = eav_category.id
            left join geo_district on ads_ad.district_id = geo_district.id
            left join geo_region on ads_ad.region_id = geo_region.id
            left join users_user on users_user.id = ads_ad.user_id
            {sql}
            order by ads_ad.created_at desc limit %s offset %s""",
            [PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_ads_list_by_categories(page, categories):
    offset = (page - 1) * PER_PAGE
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select ads_ad.*
            ,eav_category.title as category_title 
            ,geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru
            ,geo_region.name_uz as region_name_uz, geo_region.name_ru as region_name_ru 
            , (select array_agg(row_to_json(qaz)) from (
            select eav_attribute.id, eav_attribute.properties->>'label' as "label", eav_attribute.slug, 
            case when eav_value."label" is not null then eav_value."label" 
            else jsonb_build_object('label', jsonb_build_object('label_uz', ads_ad.properties->>eav_attribute.slug, 'label_ru', ads_ad.properties->>eav_attribute.slug)) 
            end as value_label
            from eav_attribute 
            left join eav_attributevalue on eav_attribute.id = eav_attributevalue.attribute_id
            left join eav_value on eav_attributevalue.value_id = eav_value.id
            left join eav_inputtype on eav_attribute.input_type_id = eav_inputtype.id
            where (eav_value.id::text = ads_ad.properties->>eav_attribute.slug or eav_value."label" is null) and eav_attribute.slug in (select jsonb_object_keys(ads_ad.properties))) qaz) as fields
            from ads_ad
            inner join eav_category on ads_ad.category_id = eav_category.id
            left join geo_district on ads_ad.district_id = geo_district.id
            left join geo_region on ads_ad.region_id = geo_region.id
            where ads_ad.category_id in %s
            order by ads_ad.created_at desc limit %s offset %s""",
            [tuple(categories), PER_PAGE, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_ads_count(sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM ads_ad            
                            left join users_user on users_user.id = ads_ad.user_id
                            {sql}
                        """)
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


def _query_ads_count_by_categories(categories):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM ads_ad where category_id in %s""", [tuple(categories)])
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result


"""CATEGORY FIELDS"""


def get_category_fields(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_attribute.id, eav_attribute.slug, eav_attribute.properties->>'data_type' as data_type, (eav_attribute.properties->>'validation')::json->>'rule' as "rule", 
            (eav_attribute.properties->>'validation')::json->>'min' as "min", (eav_attribute.properties->>'validation')::json->>'max' as "max" FROM eav_entityattribute
            inner join eav_attribute on eav_attribute.id = eav_entityattribute.attribute_id 
            WHERE eav_entityattribute.entity_id in (SELECT eav_entity.id FROM eav_categoryentity INNER JOIN eav_entity 
            ON eav_categoryentity.entity_id = eav_entity.id WHERE category_id = %s ORDER BY eav_categoryentity.sorting) order by eav_entityattribute.entity_id;
            """, [category_id]
        )
        rows = dictfetchall(cursor)
    return rows

