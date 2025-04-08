from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^list/$", views.TarifView.as_view(), name="tarifs-list")
    ]
