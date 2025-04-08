from django.urls import include, re_path
from elon.api.tg.ads import views

urlpatterns = [
    re_path(r"^list/$", views.AdView.as_view(), name="ads-list"),
    re_path(r"^create/$", views.AdView.as_view(), name="ad-create"),
    re_path(r"^by/(?P<category_id>[0-9]+)/categories/$", views.AdView.as_view(), name="ads-by-categories"),
    re_path(r"^(?P<pk>[0-9]+)/info/$", views.AdView.as_view(), name="ad-info"),
    re_path(r"^(?P<pk>[0-9]+)/sent/$", views.AdView.as_view(), name="ad-sent"),
    re_path(r"^(?P<pk>[0-9]+)/delete/$", views.AdView.as_view(), name="ad-delete"),
    re_path(r"^comment/$", views.AdCommentView.as_view(), name="ad-comment"),
]
