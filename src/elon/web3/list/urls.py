from django.urls import include, re_path
from elon.web3.list import views
from django.urls import re_path


urlpatterns = [
    re_path(r"ad/category/(?P<user_id>[\w-]+)/$", views.ad_category, name="ad-category"),
    re_path(r"view/category/(?P<category_id>[\w-]+)/(?P<user_id>[\w-]+)/$", views.category_view, name="category-view"),
    re_path(r"ad/filter/(?P<category_id>[\w-]+)/$", views.ad_filter, name="ad-filter"),
    re_path(r"ad/elon/view/(?P<ad_id>[\w-]+)/$", views.ad_view, name="ad-view"),


]
