
import re
from django import template
from elon.ads.models import CategoryService
from datetime import datetime as dt

register = template.Library()



# def get_service_ads_count(service):
#     if service.alias == "free":
#         # ads = Ad.objects.filter(status=4)
#         count = 0
#         # for ad in ads:
#         #     if not Advertised.objects.filter(ad_id=ad.id).exists():
#         #         count += 1
#     else:
#         count = Advertised.objects.filter(service=service).count()
#     return count


# register.filter('service_ads_count', get_service_ads_count)
