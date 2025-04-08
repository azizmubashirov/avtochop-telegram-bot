# -*- coding: utf-8 -*-
from django.conf import settings
from contextlib import closing
from collections import OrderedDict
from django.db import connection
from rest_framework.exceptions import NotFound
from elon.base.utils.db import dictfetchall, dictfetchone
from elon.base.utils.sqlpaginator import SqlPaginator
import json


def get_ad_one(request, pk):
    ad = _query_ad_one(pk)
    if ad:
        return OrderedDict([
            ('id', ad['id']),
            ('title', ad['title']),
            ('description', ad['description']),
            ('images', ad['images']),
            ('prices', json.loads(ad['prices'])),
            ('properties', json.loads(ad['properties']) if ad['properties'] else {}),
            ('fields', ad['fields']),
            ('user_id', ad['user_id'] if ad['user_id'] else None),
            ('contact', json.loads(ad['contact'])),
            ('category', None) if not ad['category_id'] and not ad['category_title'] else (
                'category', {
                    "id": ad['category_id'],
                    "title": json.loads(ad['category_title']),
                }
            ),
            ('region', None) if not ad['region_id'] else (
                'region', {
                    "id": ad['region_id'],
                    "name": {
                        "name_uz": ad['region_name_uz'],
                        "name_ru": ad['region_name_ru']
                    }
                }
            ),
            ('district', None) if not ad['district_id'] else (
                'district', {
                    "id": ad['district_id'],
                    "name": {
                        "name_uz": ad['district_name_uz'],
                        "name_ru": ad['district_name_ru']}
                }
            ),
            ('currency', ad['currency']),
            ('torg', ad['torg']),
            ('status', ad['status']),
            ('marka_id', ad['marka_id']),
            ('model_id', ad['model_id']),
            ('positsion_id', ad['positsion_id']),
            ('created_at', ad['created_at'].strftime("%Y-%m-%d %H:%M:%S")),
            
        ])
    else:
        raise NotFound('ad not found')




def _query_ad_one(pk):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """select ads_ad.*
            ,eav_category.title as category_title, (select row_to_json(chan) from (WITH recursive ParentOf (id, parent_id) as 
            (SELECT id, parent_id FROM eav_category WHERE id = ads_ad.category_id UNION all 
            SELECT ec.id, ec.parent_id FROM eav_category ec INNER JOIN ParentOf ON ec.id = ParentOf.parent_id) 
            SELECT id, parent_id FROM ParentOf where parent_id is null) as chan ) as channel
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


def _query_ads_list(page, per_page, sql):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select ads_ad.*
            ,eav_category.title as category_title, (select row_to_json(chan) from (WITH recursive ParentOf (id, channel_title, channel_url, parent_id) as 
            (SELECT id, channel_title, channel_url, parent_id FROM eav_category WHERE id = ads_ad.category_id UNION all 
            SELECT ec.id, ec.channel_title, ec.channel_url, ec.parent_id FROM eav_category ec INNER JOIN ParentOf ON ec.id = ParentOf.parent_id) 
            SELECT id, channel_title, channel_url, parent_id FROM ParentOf where parent_id is null) as chan ) as channel   
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
            [per_page, offset]
        )
        rows = dictfetchall(cursor)
    return rows


def _query_ads_list_by_categories(page, per_page, categories, sql):
    offset = (page - 1) * per_page
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select ads_ad.*
            ,eav_category.title as category_title, (select row_to_json(chan) from (WITH recursive ParentOf (id, channel_title, channel_url, parent_id) as 
            (SELECT id, channel_title, channel_url, parent_id FROM eav_category WHERE id = ads_ad.category_id UNION all 
            SELECT ec.id, ec.channel_title, ec.channel_url, ec.parent_id FROM eav_category ec INNER JOIN ParentOf ON ec.id = ParentOf.parent_id) 
            SELECT id, channel_title, channel_url, parent_id FROM ParentOf where parent_id is null) as chan ) as channel 
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
            where ads_ad.category_id in %s {sql}
            order by ads_ad.created_at desc limit %s offset %s""",
            [tuple(categories), per_page, offset]
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


def _query_ads_count_by_categories(categories, sql):
    with closing(connection.cursor()) as cursor:
        cursor.execute(f"""SELECT COUNT(1) as cnt FROM ads_ad where category_id in %s {sql}""", [tuple(categories)])
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
            """SELECT eav_attribute.id, eav_attribute.slug, eav_attribute.price_state, eav_attribute.properties->>'data_type' as data_type, (eav_attribute.properties->>'validation')::json->>'rule' as "rule", 
            (eav_attribute.properties->>'validation')::json->>'min' as "min", (eav_attribute.properties->>'validation')::json->>'max' as "max" FROM eav_entityattribute
            inner join eav_attribute on eav_attribute.id = eav_entityattribute.attribute_id 
            WHERE eav_entityattribute.entity_id in (SELECT eav_entity.id FROM eav_categoryentity INNER JOIN eav_entity 
            ON eav_categoryentity.entity_id = eav_entity.id WHERE category_id = %s ORDER BY eav_categoryentity.sorting) order by eav_entityattribute.entity_id;
            """, [category_id]
        )
        rows = dictfetchall(cursor)
    return rows

