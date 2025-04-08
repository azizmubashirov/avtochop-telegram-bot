# -*- coding: utf-8 -*-
from datetime import datetime as dt
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json
import re


def get_filter_ad_list(request, category):
    usd_sum = 11400
    page = 1
    per_page = settings.PER_PAGE

    user_id = request.user.id
    favourite_user_id = request.user.id
    price_from = request.POST.get('price_from', 0).replace(' ', '')
    price_to = request.POST.get('price_to', 0).replace(' ', '')
    currency = request.POST.get('currency', '')

    marka_id = request.POST.get('marka_id')
    madel_id = request.POST.get('madel_id')
    positsion_id = request.POST.get('positsion_id')

    extra_sql = "where "
    sql = ""

    if user_id:
        sql = extra_sql

    if sql:
        sql += "ads_ad.status = 4 and "
    else:
        sql += "where ads_ad.status = 4 and "

    if category:
        sql += f"ads_ad.category_id in ({str(category).strip('[ ]')}) and "
        d = []
        attribute_slug = _query_get_attribute_slug(category)
        for i in attribute_slug:
            d.append(i['slug'])
        for key, value in request.POST.items():
            if len(key.split('_%')) == 2 and key.split('_%')[0] in d and value:
                if key.split('_%')[1] == "from":
                    sql += f"ads_ad.properties ->>'{key.split('_%')[0]}' >= '{value}' and "
                elif key.split('_%')[1] == "to":
                    sql += f"ads_ad.properties ->>'{key.split('_%')[0]}' <= '{value}' and "
            elif key in d and value and value != '1a':
                sql += f"ads_ad.properties->>'{key}' = '{value}' and "

    if marka_id:
        sql += f"ads_ad.marka_id = {int(marka_id)} and "

    if madel_id:
        sql += f"ads_ad.model_id = {int(madel_id)} and "

    if positsion_id:
        sql += f"ads_ad.positsion_id = {int(positsion_id)} and "

    price = f"* {usd_sum}"
    sort = ' ads_ad.created_at desc, ads_ad.id desc'

    if price_from and price_to and price_from != '0' and price_to != '0':
        curren = currency if currency else 1
        price_from = int(price_from) if int(curren) == 1 else int(price_from) * usd_sum
        price_to = int(price_to) if int(curren) == 1 else int(price_to) * usd_sum
        sql += "where " if not sql else ""
        sql += f"{price_from} <= pricess.price and pricess.price <= {price_to} and "
    elif price_from and price_from != '0':
        curren = currency if currency else 1
        price_from = int(price_from) if int(curren) == 1 else int(price_from) * usd_sum
        sql += "where " if not sql else ""
        sql += f"{price_from} <= pricess.price and "
    elif price_to and price_to != '0':
        curren = currency if currency else 1
        price_to = int(price_to) if int(curren) == 1 else int(price_to) * usd_sum
        sql += "where " if not sql else ""
        sql += f"pricess.price <= {price_to} and "

    sql = sql.strip("and ")

    count_records = _query_ads_count(sql, usd_sum=usd_sum)
    ads = _query_ads_list(page, per_page, sql, favourite_user_id, sort=sort, usd_sum=usd_sum)

    items = []
    price_type = currency
    currency = ''
    for ad in ads:
        if json.loads(ad['prices']):
            if json.loads(ad['prices']).get('narx') or json.loads(ad['prices']).get('narx') == 0:
                price_currency = int(json.loads(ad['prices']).get('narx'))
                if ad.get('currency'):
                    currency = "so'm" if ad.get("currency") == 1 else "y.e"
                if ad.get('currency') and price_type:
                    if int(price_type) == 1:
                        price_currency = price_currency if ad.get('currency') == int(
                            price_type) else price_currency * usd_sum
                    elif int(price_type) == 2:
                        price_currency = price_currency if ad.get('currency') == 2 else price_currency / usd_sum
                currency = currency if not price_type else "y.e" if int(price_type) == 2 else "so'm" if int(
                    price_type) == 1 else currency
                narx = price_format(price_currency) if price_currency > 1 else f"{str(price_currency)[:4]}"
                price = f"{narx} {currency}"
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
            ('created_at', {'uz': format_date(ad['created_at'], 'uz'), 'ru': format_date(ad['created_at'], 'ru')}),
        ]))
    paginator = SqlPaginator(request, page=page, per_page=per_page, count=count_records)
    paging = paginator.get_paginated_response()
    return OrderedDict([
        ('items', items),
        ('meta', paging)
    ])


def _query_ads_list(page, per_page, sql, favourite_user_id, sort='ads_ad.created_at desc, ads_ad.id desc', usd_sum=11400):
    print(sql)
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
            , (select exists (select * from ads_adfavourite where ads_adfavourite.ad_id = ads_ad.id and ads_adfavourite.user_id = %s and ads_adfavourite.status = 1)) as favourite 
            , (select case when payment_orders.status = 3 then true else false end as freee from payment_orders where payment_orders.ad_id = ads_ad.id order by payment_orders.created desc limit 1) as is_payed 
            from ads_ad
            inner join eav_category on ads_ad.category_id = eav_category.id
            left join eav_category as ec2 on ec2.id = eav_category.parent_id
            left join geo_district on ads_ad.district_id = geo_district.id
            left join geo_region on ads_ad.region_id = geo_region.id
            left join users_user on users_user.id = ads_ad.user_id
            left join(select ads_ad.id,ads_ad.created_at, 
                case
                    when ads_ad.currency = 1 and ads_ad.prices->>'from' is not null   then cast(ads_ad.prices->>'from' AS bigint)
                    when ads_ad.currency = 1 and ads_ad.prices->>'from' is null  then cast(ads_ad.prices->>'narx' AS bigint)
                    when ads_ad.currency = 2 and ads_ad.prices->>'from' is not null   then cast(ads_ad.prices->>'from' AS bigint) * {usd_sum}
                    when ads_ad.currency = 2 and ads_ad.prices->>'from' is null  then cast(ads_ad.prices->>'narx' AS bigint) * {usd_sum}
                else 
                    cast(ads_ad.prices->>'narx' AS bigint)
                end as price from ads_ad) as pricess on pricess.id=ads_ad.id
            {sql}
            order by {sort} limit %s offset %s""",
            [favourite_user_id, per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows



def _query_ads_count(sql, usd_sum=11400):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM ads_ad            
                            left join users_user on users_user.id = ads_ad.user_id
                            left join(select ads_ad.id,ads_ad.created_at, 
                                case
                                    when ads_ad.currency = 1 and ads_ad.prices->>'from' is not null   then cast(ads_ad.prices->>'from' AS bigint)
                                    when ads_ad.currency = 1 and ads_ad.prices->>'from' is null  then cast(ads_ad.prices->>'narx' AS bigint)
                                    when ads_ad.currency = 2 and ads_ad.prices->>'from' is not null   then cast(ads_ad.prices->>'from' AS bigint) * {usd_sum}
                                    when ads_ad.currency = 2 and ads_ad.prices->>'from' is null  then cast(ads_ad.prices->>'narx' AS bigint) * {usd_sum}
                                else 
                                    cast(ads_ad.prices->>'narx' AS bigint)
                            end as price from ads_ad) as pricess on pricess.id=ads_ad.id
                            {sql}
                        """)
        row = dictfetchone(cursor)
    if row:
        result = row['cnt']
    else:
        result = 0
    return result



def _query_get_region_one(region):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""select id from geo_region where slug = %s""", [region])
        row = dictfetchone(cursor)
    return row


def _query_get_attribute_slug(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute("""select ea.slug, ea.id 
                from eav_category ec 
                inner join eav_categoryentity ec2 on ec.id = ec2.category_id 
                inner join eav_entityattribute ee on ec2.entity_id = ee.entity_id
                inner join eav_attribute ea on ee.attribute_id = ea.id 
                where ec.id = %s""", [category_id])
        row = dictfetchall(cursor)
    return row


def price_format(inp):
    price_float = str(inp).split('.')
    price = int(price_float[0])
    try:
        price_float = f".{price_float[1][:2]}" if len(price_float) == 2 else f""
    except:
        price_float = ''
    res = "{:,}".format(price)
    formated = re.sub(",", " ", res)

    return f"{formated}{price_float}"


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
            delta = dt(int(today[0]), int(today[1]), int(today[2])) - dt(int(full_date[0].split("-")[0]),
                                                                         int(full_date[0].split("-")[1]),
                                                                         int(full_date[0].split("-")[2]))
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
