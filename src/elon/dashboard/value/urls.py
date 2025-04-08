from django.urls import include, path
from elon.dashboard.value import views


urlpatterns = [
    path("value/list/", views.value_list, name="value-list"),
    path("value/create/", views.value_create, name="value-create"),
    path("value/<int:value_id>/edit/", views.value_edit, name="value-edit"),
    path("value/<int:value_id>/delete/", views.value_delete, name="value-delete"),
]
