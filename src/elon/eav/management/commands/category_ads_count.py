from django.core.management.base import BaseCommand
from eelon.eav.models import Category
from django.db import connection
from eelon.base.utils.db import dictfetchall, dictfetchone
from contextlib import closing


def get_category_ads_count(category_id):
    with closing(connection.cursor()) as cursor:
        cursor.execute(
            """SELECT count(1) as cnt FROM ads_ad aa WHERE aa.status = 4 AND aa.category_id = %s;""", [category_id]
        )
        row = dictfetchone(cursor)
    return int(row.get("cnt", 0))


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print("Category Ads Counting Started!")
        categories = Category.objects.all()
        for category in categories:
            ads_count = get_category_ads_count(category.id)
            category.ads_count = ads_count
            category.save()
        print("Category Ads Counting Ended!")
