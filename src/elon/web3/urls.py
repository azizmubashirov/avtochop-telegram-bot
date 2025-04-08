from django.urls import include, path
from elon.web3.ads import urls as ads_urls
from elon.web3.payment import urls as payment_urls
from elon.web3.list import urls as view_urls
from elon.web3.my_ads import urls as my_urls
from elon.web3.favourite import urls as favourite_urls
from elon.web3.profile import urls as profile_urls
from .views import search_model

app_name = "web3"

urlpatterns = [
    path("", include(ads_urls)),
    path("", include(payment_urls)),
    path("", include(view_urls)),
    path("", include(my_urls)),
    path("", include(favourite_urls)),
    path("", include(profile_urls)),
    path("search-model", search_model, name='search-model'),
    
]
