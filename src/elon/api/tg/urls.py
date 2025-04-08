from django.urls import include, path
from elon.api.tg.eav import urls as eav_urls
# from elon.api.tg.ads import urls as ads_urls
# from elon.api.tg.users import urls as user_urls

app_name = "tg"

urlpatterns = [
    path("eav/", include(eav_urls)),
]
