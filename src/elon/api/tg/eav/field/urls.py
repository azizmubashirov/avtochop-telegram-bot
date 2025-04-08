from django.urls import include, re_path
from elon.api.tg.eav.field import views

urlpatterns = [
    re_path(r"^(?P<pk>[0-9]+)/marka/$", views.FieldView.as_view(), name="marka-view"),
    re_path(r"^(?P<category_slug>[\w-]+)/marka/$", views.FieldView.as_view(), name="marka-view-slug"),
    re_path(r"^mark/(?P<mark_id>[0-9]+)/info/$", views.FieldView.as_view(), name="marka-info"),
    re_path(r"^(?P<pk>[0-9]+)/madel/$", views.FieldView.as_view(), name="madel-view"),
    re_path(r"^(?P<marka_slug>[\w-]+)/madel/$", views.FieldView.as_view(), name="madel-view-slug"),
    re_path(r"^madel/(?P<madel_id>[0-9]+)/info/$", views.FieldView.as_view(), name="madel-info"),
    re_path(r"^(?P<pk>[0-9]+)/positsion/$", views.FieldView.as_view(), name="positsion-view"),
    re_path(r"^(?P<madel_slug>[\w-]+)/positsion/$", views.FieldView.as_view(), name="positsion-view-slug"),
    re_path(r"^positsion/(?P<pos_id>[0-9]+)/info/$", views.FieldView.as_view(), name="positsion-info"),
]

