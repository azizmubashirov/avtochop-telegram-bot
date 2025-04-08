from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r"^region/$", views.RegionView.as_view(), name="region"),
    re_path(r"^region/(?P<pk>[0-9]+)/info/$", views.RegionView.as_view(), name="region-info"),
    re_path(r"^region/(?P<pk>[0-9]+)/children/$", views.RegionView.as_view(), name="region-children"),
    re_path(r"^district/$", views.DistrictView.as_view(), name="district-create"),
    re_path(r"^district/(?P<pk>[0-9]+)/info/$", views.DistrictView.as_view(), name="district-info"),
]

