from django.urls import include, path
from elon.dashboard.attribute import views


urlpatterns = [
    path("attribute/list/", views.attribute_list, name="attribute-list"),
    path("attribute/create/", views.attribute_create, name="attribute-create"),
    path("attribute/<int:attribute_id>/edit/", views.attribute_edit, name="attribute-edit"),
    path("attribute/<int:attribute_id>/delete/", views.attribute_delete, name="attribute-delete"),
]
