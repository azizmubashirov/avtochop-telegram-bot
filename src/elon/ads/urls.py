from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^ads/$", views.AdView.as_view(), name="ad-create"),
    url(r"^ads/(?P<category_id>[0-9]+)/categories/$", views.AdView.as_view(), name="ads-by-categories"),
    url(r"^ads/(?P<pk>[0-9]+)/info/$", views.AdView.as_view(), name="ad-info"),
]

