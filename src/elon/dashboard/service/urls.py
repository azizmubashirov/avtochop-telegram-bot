from django.urls import include, path
from elon.dashboard.service import views


urlpatterns = [
    path("service/list/", views.service_list, name="service-list"),
    path("service/create/", views.service_create, name="service-create"),
    path("service/<int:service_id>/edit/", views.service_edit, name="service-edit"),
    path("service/<int:service_id>/delete/", views.service_delete, name="service-delete"),
]
