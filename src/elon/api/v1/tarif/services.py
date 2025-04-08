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


def get_services(services_alias, category_id):
    categories = _query_tarif(services_alias, category_id)
    items = []
    for data in categories:
        items.append(OrderedDict([
            ('id', data['id']),
            ('title', json.loads(data['title'])),
            ('service', json.loads(data['services'])),
            ('description', json.loads(data['description'])),
            ('alias', data['alias']),
            ('price', data['price']),
        ]))
    return OrderedDict([
        ('items', items)
        ])


def _query_tarif(services_alias, category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            f"""select payment_service.id, payment_service.title, ads_categoryservice.price, payment_service.alias, 
            payment_service.services, payment_service.description
                from ads_categoryservice
                inner join payment_service on ads_categoryservice.service_id = payment_service.id
                where ads_categoryservice.category_id = %s
                and payment_service.alias in %s order by payment_service.sort_order""", [category_id, tuple(services_alias)]
        )
        rows = dictfetchall(cursor)
    return rows