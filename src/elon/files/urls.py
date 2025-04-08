from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r"^upload/$", views.FileView.as_view(), name="file-upload"),
    re_path(r"^(?P<pk>[0-9]+)/$", views.FileView.as_view(), name="file-get"),
]

