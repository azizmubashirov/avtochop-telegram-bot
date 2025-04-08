from django.urls import include, re_path
from elon.api.v1.eav.value import views

urlpatterns = [
    re_path(r"^value/list/$", views.ValueView.as_view(), name="value-list"),
    re_path(r"^value/create/$", views.ValueView.as_view(), name="value-create"),
    re_path(r"^value/(?P<pk>[0-9]+)/info/$", views.ValueView.as_view(), name="value-info"),
    re_path(r"^attribute-value/$", views.AttributeValueView.as_view(), name="attribute-value-create"),
    re_path(r"^attribute-value/(?P<pk>[0-9]+)/info/$", views.AttributeValueView.as_view(), name="attribute-value-info"),
]

