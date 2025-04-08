from django.urls import include, re_path
from elon.web3.favourite import views
from django.urls import re_path


urlpatterns = [
    re_path(r"ad/favourite/(?P<user_id>[\w-]+)/$", views.ad_favourite, name="ad-favourite"),
]
