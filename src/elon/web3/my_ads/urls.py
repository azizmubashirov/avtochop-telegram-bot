from django.urls import include, re_path
from elon.web3.my_ads import views
from django.urls import re_path


urlpatterns = [
    re_path(r"my/ads/ajax/$", views.my_ajax, name="my-ads-ajax"),
    
    re_path(r"my/ads/(?P<user_id>[\w-]+)/$", views.my_ads, name="my-ads"),
    re_path(r"my/ads/active/(?P<user_id>[\w-]+)/$", views.my_ads_active, name="my-ads-active"),
    re_path(r"my/ads/process/(?P<user_id>[\w-]+)/$", views.my_ads_process, name="my-ads-process"),
    re_path(r"my/ads/refused/(?P<user_id>[\w-]+)/$", views.my_ads_refused, name="my-ads-refused"),
]
