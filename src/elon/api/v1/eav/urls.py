from django.urls import path, include
from elon.api.v1.eav.category import urls as category_urls
from elon.api.v1.eav.value import urls as value_urls


urlpatterns = [
    path('', include(category_urls)),
]
