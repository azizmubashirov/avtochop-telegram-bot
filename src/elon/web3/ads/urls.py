from django.urls import include, re_path
from elon.web3.ads import views
from django.urls import re_path


urlpatterns = [
    re_path(r"ads/create/(?P<user_id>[\w-]+)/$", views.ads_create, name="ads-create"),
    re_path(r"add/category/(?P<user_id>[\w-]+)/$", views.add_category, name="add-category"),
    re_path(r"add/marka/(?P<category_id>[\w-]+)/$", views.add_marka, name="add-marka"),
    re_path(r"add/model/(?P<marka_id>[\w-]+)/$", views.add_model, name="add-model"),
    re_path(r"add/positsion/(?P<model_id>[\w-]+)/$", views.add_positsion, name="add-positsion"),
    re_path(r"add/properties/(?P<positsion_id>[\w-]+)/$", views.add_properties, name="add-properties-id"),
    re_path(r"add/properties/$", views.add_properties, name="add-properties"),
    re_path(r"add/description/$", views.add_description, name="add-description"),
    re_path(r"add/photo/$", views.add_photo, name="add-photo"),
    re_path(r"add/price/$", views.add_price, name="add-price"),
    re_path(r"add/region/$", views.add_region, name="add-region"),
    re_path(r"add/district/(?P<region_id>[\w-]+)/$", views.add_district, name="add-district"),
    re_path(r"add/phone/(?P<district_id>[\w-]+)/$", views.add_phone, name="add-phone"),
    re_path(r"add/phone/$", views.add_phone, name="add-phone-id"),
    re_path(r"ads/view/$", views.ads_view, name="ads-view"),

    re_path(r"ad/success/$", views.ad_success, name="ad-success"),

    re_path(r"add/ajax/$", views.add_ajax, name="add-ajax"),
]
