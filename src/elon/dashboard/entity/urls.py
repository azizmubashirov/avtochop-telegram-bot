from django.urls import include, path
from elon.dashboard.entity import views


urlpatterns = [
    path("entity/list/", views.entity_list, name="entity-list"),
    path("entity/create/", views.entity_create, name="entity-create"),
    path("entity/<int:entity_id>/edit/", views.entity_edit, name="entity-edit"),
    path("entity/<int:entity_id>/delete/", views.entity_delete, name="entity-delete"),
]
