from django.urls import include, path
from elon.dashboard.ads import views


urlpatterns = [
    path("elon/list/", views.ads_list, name="ads-list"),
    path("elon/create/", views.ads_create, name="ads-create"),
    # path("elon/<int:user_id>/create/", views.ads_create, name="ads-create-by-user"),
    path("elon/<int:ad_id>/edit/", views.ads_edit, name="ads-edit"),
    path("elon/<int:ad_id>/delete/", views.ads_delete, name="ads-delete"),
    path("elon/<int:ad_id>/submit/", views.ads_submit, name="ads-submit"),
    path("elon/<int:ad_id>/refuse/", views.ads_refuse, name="ads-refuse"),
    path("elon/<int:ad_id>/view/", views.ads_view, name="ads-view"),
    path("elon/field/", views.ads_field, name="ads-field"),
    # path("complain/elon/list/", views.complain_ads, name="complain-elon-list"),
]
