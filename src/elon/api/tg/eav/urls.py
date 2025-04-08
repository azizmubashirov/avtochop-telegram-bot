from django.urls import path, include
from elon.api.tg.eav.field import urls as field_urls


urlpatterns = [
    path('field/', include(field_urls)),
]
