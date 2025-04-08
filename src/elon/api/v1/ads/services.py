# -*- coding: utf-8 -*-
from datetime import datetime as dt
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json
import re
import datetime


def get_user_ads(request, user_id):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.DASHBOARD_PAGINATE_BY))
    except:
        page = 1
        per_page = settings.DASHBOARD_PAGINATE_BY

    favourite_user_id = request.query_params.get('favourite_user', 0)
    sql = ""
    count_records = _query_ads_count(sql)
    ads = _query_user_ads_list(page, per_page, user_id)
    items = []
    currency = ''
    for ad in ads:
        if ad['data']['prices']:
            if ad['data']['prices'].get('narx') or ad['data']['prices'].get('narx') == 0:
                if ad.get('data').get('currency'):
                    currency = "so'm" if ad.get('data').get("currency") == 1 else "y.e"
                narx = price_format(ad['data']['prices'].get('narx')) if str(ad['data']['prices'].get('narx')).isdigit() else '--'
                ad['data']['price_txt'] = f"{narx} {currency}"
            elif ad['data']['prices'].get('from') and ad['data']['prices'].get('to'):
                if ad.get('data').get('currency'):
                    currency = "so'm" if ad.get('data').get("currency") == 1 else "y.e"
                from_price = price_format(ad['data']['prices'].get('from')) if str(ad['data']['prices'].get('from')).isdigit() else '--'
                to_price = price_format(ad['data']['prices'].get('to')) if str(ad['data']['prices'].get('to')).isdigit() else '--'
                ad['data']['price_txt'] = f"{from_price}-{to_price} {currency}"
        items.append(OrderedDict([
            ('id', ad['id']),
            ('category_slug', ad['category_slug']),
            ('comment', ad['comment']),
            ('region_slug', ad['region_slug']),
            ('parent_slug', ad['parent_slug']),
            ('data', ad['data'])
            ]))


    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def get_ad_list(request, categories=0):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))
    except:
        page = 1
        per_page = settings.PER_PAGE
    
    favourite_user = request.user.id

    sql = "where ads_ad.status = 4 and "

    if categories:
        sql += f"ads_ad.category_id = {categories} and "

    sql = sql.strip("and ")
    count_records = _query_ads_count(sql)
    ads = _query_ads_list(page, per_page, sql, favourite_user)
    items = []
    currency = ''
    for ad in ads:
        fields = ad['fields']
        if ad.get('marka'):
            fields.insert(0, ad.get('marka'))
        if ad.get('model'):
            fields.insert(1, ad.get('model'))
        if ad.get('positsion'):
            fields.insert(2, ad.get('positsion'))
        items.append(OrderedDict([
            ('id', ad['id']),
            ('title', ad['title']),
            ('slug', ad['slug']),
            ('description', ad['description']),
            ('images', ad['images']),
            ('prices', json.loads(ad['prices'])),
            ('properties', json.loads(ad['properties']) if ad['properties'] else {}),
            ('fields', ad['fields']),
            ('views_count', ad['views_count']),
            ('favourite', ad['favourite']),
            ('user_id', ad['user_id'] if ad['user_id'] else None),
            ('contact', json.loads(ad['contact'])),
            ('category', None) if not ad['category_id'] and not ad['category_title'] else (
                'category', {
                    "id": ad['category_id'],
                    "title": json.loads(ad['category_title']),
                    "slug": ad['category_slug'],
                    'parent_slug': ad.get('parent_slug', '')
                }
            ),
            ('region', None) if not ad['region_id'] else (
                'region', {
                    "id": ad['region_id'],
                    "name": {
                        "name_uz": ad['region_name_uz'],
                        "name_ru": ad['region_name_ru']
                    },
                    "slug": ad['region_slug']
                }
            ),
            ('district', None) if not ad['district_id'] else (
                'district', {
                    "id": ad['district_id'],
                    "name": {
                        "name_uz": ad['district_name_uz'],
                        "name_ru": ad['district_name_ru']
                    }
                }
            ),
            ('currency', ad['currency']),
            ('status', ad['status']),
            ('mark', ad['marka_id']),
            ('model', ad['model_id']),
            ('positsion', ad['positsion_id']),
            ('comment', ad['ad_comment']),
            ('created_at', {'uz':format_date(ad['created_at'], 'uz'),'ru':format_date(ad['created_at'], 'ru')} ),
        ]))


    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def _query_user_ads_list(page, per_page, user_id):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
                f"""select ads_ad.id, eav_category.slug as category_slug,ads_adcomment."comment",geo_region.slug as region_slug, ec2.slug as parent_slug , json_build_object(
                    'tarif_title', array_agg(at2.title),
                    'title', ads_ad.title ,
                    'properties', ads_ad.properties,
                    'slug', ads_ad.slug,
                    'images', ads_ad.images,
                    'prices', ads_ad.prices,
                    'price_txt', ads_ad.price_txt,
                    'views_count', ads_ad.views_count,
                    'user_id', ads_ad.user_id,
                    'currency', ads_ad.currency,
                    'status', ads_ad.status,
                    'created_at', to_char(ads_ad.created_at, 'Mon dd, yyyy HH24:MI')
                    
                ) as "data"
                from ads_ad
                inner join eav_category on ads_ad.category_id = eav_category.id
                left join eav_category as ec2 on ec2.id = eav_category.parent_id
                left join users_user on users_user.id = ads_ad.user_id
                left join ads_adcomment on ads_ad.id = ads_adcomment.ad_id
                left join geo_region on ads_ad.region_id = geo_region.id
                left join ads_adsplan aa2 on ads_ad.id = aa2.ads_id
                left join ads_tarif at2 on aa2.tarif_id = at2.id 
                where ads_ad.user_id = %s
                group by ads_ad.id, eav_category.slug, ads_adcomment."comment", region_slug ,parent_slug
                order by ads_ad.id desc limit %s offset %s""",
            [user_id, per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows

def _query_ads_count(sql, is_home=False):
    if is_home:
        a = f"and '{dt.now()}' between aa.home_start and aa.home_end"
    else:
        a = ''
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM ads_ad            
                            left join users_user on users_user.id = ads_ad.user_id
                            {sql} {a}
                        """)
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result

def _query_ads_list(page, per_page, sql, favourite_user_id):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select
                ads_ad.*, ads_adcomment.comment as ad_comment
                ,eav_category.title as category_title, eav_category.slug as category_slug, ec2.slug as parent_slug 
                ,geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru 
                ,geo_region.name_uz as region_name_uz, geo_region.name_ru as region_name_ru, geo_region.slug as region_slug 
                ,(select array_agg(row_to_json(qaz)) from (
                select eav_attribute.properties->'title'->>'title_uz' as "title", 
                case when eav_value."label" is not null then eav_value."label"->'label_uz'
                else ads_ad.properties->eav_attribute.slug
                end as value
                from eav_attribute
                left join eav_attributevalue on eav_attribute.id = eav_attributevalue.attribute_id
                left join eav_value on eav_attributevalue.value_id = eav_value.id
                left join eav_inputtype on eav_attribute.input_type_id = eav_inputtype.id
                where (eav_value.id::text = ads_ad.properties->>eav_attribute.slug or eav_value."label" is null) and eav_attribute.slug in (select jsonb_object_keys(ads_ad.properties)) and eav_attribute.is_price = false) qaz) as fields
                ,(select json_build_object('title', 'Marka', 'value', eav_marka."label"->'label_uz') from eav_marka where eav_marka.id = ads_ad.marka_id) as marka
                ,(select json_build_object('title', 'Model', 'value', eav_model."label"->'label_uz') from eav_model where eav_model.id = ads_ad.model_id) as model
                ,(select json_build_object('title', 'Positsiya', 'value', eav_positsion."label"->'label_uz') from eav_positsion where eav_positsion.id = ads_ad.positsion_id) as positsion
                , (select exists (select * from ads_adfavourite where ads_adfavourite.ad_id = ads_ad.id and ads_adfavourite.user_id = %s and ads_adfavourite.status = 1)) as favourite 
                , (select case when payment_orders.status = 3 then true else false end as freee from payment_orders where payment_orders.ad_id = ads_ad.id order by payment_orders.created desc limit 1) as is_payed 
                from ads_ad
                inner join eav_category on ads_ad.category_id = eav_category.id
                left join eav_category as ec2 on ec2.id = eav_category.parent_id
                left join geo_district on ads_ad.district_id = geo_district.id
                left join geo_region on ads_ad.region_id = geo_region.id
                left join users_user on users_user.id = ads_ad.user_id
                left join ads_adcomment on ads_ad.id = ads_adcomment.ad_id
                {sql}
                order by ads_ad.id desc, ads_ad.id desc limit %s offset %s""",
            [favourite_user_id, per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows
"""CATEGORY FIELDS"""

def get_category_fields(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT eav_attribute.id, eav_attribute.slug, eav_attribute.properties->>'data_type' as data_type, eav_attribute.properties->>'multiple' as multiple, (eav_attribute.properties->>'validation')::json->>'rule' as "rule", 
            (eav_attribute.properties->>'validation')::json->>'min' as "min", (eav_attribute.properties->>'validation')::json->>'max' as "max" FROM eav_entityattribute
            inner join eav_attribute on eav_attribute.id = eav_entityattribute.attribute_id 
            WHERE eav_entityattribute.entity_id in (SELECT eav_entity.id FROM eav_categoryentity INNER JOIN eav_entity 
            ON eav_categoryentity.entity_id = eav_entity.id WHERE category_id = %s ORDER BY eav_categoryentity.sorting) order by eav_entityattribute.entity_id;
            """, [category_id]
        )
        rows = dictfetchall(cursor)
    return rows

def get_favourite_ad_list(request, user_id):
    try:
        page = int(request.query_params.get('page', 1))
        per_page = int(request.query_params.get('per_page', settings.PER_PAGE))
    except:
        page = 1
        per_page = settings.PER_PAGE

    count_records = _query_favourite_ads_count(user_id)
    ads = _query_favourite_ads_list(page, per_page, user_id)
    items = []

    for ad in ads:
        fields = ad['fields']
        if ad.get('marka'):
            fields.insert(0, ad.get('marka'))
        if ad.get('model'):
            fields.insert(1, ad.get('model'))
        if ad.get('positsion'):
            fields.insert(2, ad.get('positsion'))
        items.append(OrderedDict([
            ('id', ad['id']),
            ('title', ad['title']),
            ('slug', ad['slug']),
            ('description', ad['description']),
            ('images', ad['images']),
            ('prices', json.loads(ad['prices'])),
            ('properties', json.loads(ad['properties']) if ad['properties'] else {}),
            ('fields', ad['fields']),
            ('views_count', ad['views_count']),
            ('user_id', ad['user_id'] if ad['user_id'] else None),
            ('contact', json.loads(ad['contact'])),
            ('category', None) if not ad['category_id'] and not ad['category_title'] else (
                'category', {
                    "id": ad['category_id'],
                    "title": json.loads(ad['category_title']),
                    "slug": ad['category_slug'],
                    'parent_slug': ad.get('parent_slug', '')
                }
            ),
            ('region', None) if not ad['region_id'] else (
                'region', {
                    "id": ad['region_id'],
                    "name": {
                        "name_uz": ad['region_name_uz'],
                        "name_ru": ad['region_name_ru']
                    },
                    "slug": ad['region_slug']
                }
            ),
            ('district', None) if not ad['district_id'] else (
                'district', {
                    "id": ad['district_id'],
                    "name": {
                        "name_uz": ad['district_name_uz'],
                        "name_ru": ad['district_name_ru']
                    }
                }
            ),
            ('currency', ad['currency']),
            ('status', ad['status']),
            ('mark', ad['marka_id']),
            ('model', ad['model_id']),
            ('positsion', ad['positsion_id']),
            ('created_at', {'uz':format_date(ad['created_at'], 'uz'),'ru':format_date(ad['created_at'], 'ru')} ),
        ]))

    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])

def _query_favourite_ads_list(page, per_page, user_id):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select 
                    ads_ad.*
                    ,eav_category.title as category_title, eav_category.slug as category_slug, ec2.slug as parent_slug
                    ,geo_district.name_uz as district_name_uz, geo_district.name_ru as district_name_ru 
                    ,geo_region.name_uz as region_name_uz, geo_region.name_ru as region_name_ru, geo_region.slug as region_slug
                    ,(select array_agg(row_to_json(qaz)) from (
                    select eav_attribute.properties->'title'->>'title_uz' as "title", 
                    case when eav_value."label" is not null then eav_value."label"->'label_uz'
                    else ads_ad.properties->eav_attribute.slug
                    end as value
                    from eav_attribute
                    left join eav_attributevalue on eav_attribute.id = eav_attributevalue.attribute_id
                    left join eav_value on eav_attributevalue.value_id = eav_value.id
                    left join eav_inputtype on eav_attribute.input_type_id = eav_inputtype.id
                    where (eav_value.id::text = ads_ad.properties->>eav_attribute.slug or eav_value."label" is null) and eav_attribute.slug in (select jsonb_object_keys(ads_ad.properties)) and eav_attribute.is_price = false) qaz) as fields
                    ,(select json_build_object('title', 'Marka', 'value', eav_marka."label"->'label_uz') from eav_marka where eav_marka.id = ads_ad.marka_id) as marka
                    ,(select json_build_object('title', 'Model', 'value', eav_model."label"->'label_uz') from eav_model where eav_model.id = ads_ad.model_id) as model
                    ,(select json_build_object('title', 'Positsiya', 'value', eav_positsion."label"->'label_uz') from eav_positsion where eav_positsion.id = ads_ad.positsion_id) as positsion
                    from ads_ad
                    inner join eav_category on ads_ad.category_id = eav_category.id
                    left join eav_category as ec2 on ec2.id = eav_category.parent_id
                    inner join ads_adfavourite on ads_ad.id = ads_adfavourite.ad_id
                    left join geo_district on ads_ad.district_id = geo_district.id
                    left join geo_region on ads_ad.region_id = geo_region.id
                    left join users_user on users_user.id = ads_ad.user_id
                    where ads_adfavourite.user_id = {user_id} and ads_adfavourite.status = 1
                    order by ads_ad.created_at desc  limit %s offset %s""",
            [per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows

def _query_favourite_ads_count(user_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""SELECT COUNT(1) as cnt FROM ads_ad
            inner join eav_category on ads_ad.category_id = eav_category.id
            inner join ads_adfavourite on ads_ad.id = ads_adfavourite.ad_id
            where ads_adfavourite.user_id = {user_id} and ads_adfavourite.status = 1"""
        )
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result

def price_format(inp):
    price = int(inp)
    res = "{:,}".format(price)
    formated = re.sub(",", " ", res)
    return formated

def format_date(full_date, lang=None):
    months = {
        1: "yanvar" if lang == 'uz' else 'январь',
        2: "fevral" if lang == 'uz' else 'февраль',
        3: "mart" if lang == 'uz' else 'март',
        4: "aprel" if lang == 'uz' else 'апрель',
        5: "may" if lang == 'uz' else 'мая',
        6: "iyun" if lang == 'uz' else 'июнь',
        7: "iyul" if lang == 'uz' else 'июль',
        8: "avgust" if lang == 'uz' else 'август',
        9: "sentabr" if lang == 'uz' else 'сентябрь',
        10: "oktabr" if lang == 'uz' else 'Октябрь',
        11: "noyabr" if lang == 'uz' else 'ноябрь',
        12: "dekabr" if lang == 'uz' else 'Декабрь',
    }
    try:
        if full_date:
            today = dt.now().strftime("%Y-%m-%d")
            today = str(today).split("-")
            full_date = str(full_date).split()
            delta = dt(int(today[0]), int(today[1]), int(today[2])) - dt(int(full_date[0].split("-")[0]), int(full_date[0].split("-")[1]), int(full_date[0].split("-")[2]))
            delta = delta.days
            if today == full_date[0].split("-"):
                day = "Bugun " if lang == 'uz' else "Сегодня "
                formatted_date = day + full_date[1].split(":")[0] + ":" + full_date[1].split(":")[1]
            elif delta == 1:
                day = "Kecha " if lang == 'uz' else "Вчера "
                formatted_date = day + full_date[1].split(":")[0] + ":" + full_date[1].split(":")[1]
            elif today and today[0] == full_date[0].split("-")[0]:
                formatted_date = f"{full_date[1].split(':')[0]}:{full_date[1].split(':')[1]} / {int(full_date[0].split('-')[2])}-{months[int(full_date[0].split('-')[1])]}"
            else:
                formatted_date = full_date[1].split(":")[0] + ":" + full_date[1].split(":")[1]
                formatted_date = formatted_date + " / " + full_date[0]
        else:
            formatted_date = None
        return formatted_date
    except Exception as e:
        return full_date

   