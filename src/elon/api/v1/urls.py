from django.urls import include, path
from elon.api.v1.users import urls as users_urls
from elon.api.v1.eav import urls as eav_urls
from elon.api.v1.ads import urls as items_urls
from elon.api.v1.payment import urls as payment_urls
from elon.api.v1.tarif import urls as tarif_urls
from elon.files import urls as file_urls
from elon.geo import urls as geo_urls


app_name = "api"
urlpatterns = [
    path("users/", include(users_urls)),
    path("eav/", include(eav_urls)),
    path("file/", include(file_urls)),
    path("payment/", include(payment_urls)),
    path("geo/", include(geo_urls)),
    path("service/", include(tarif_urls)),
    path("items/", include(items_urls)),
]
