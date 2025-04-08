from django.urls import include, path
from elon.dashboard.category import views


urlpatterns = [
    path("category/list/", views.category_list, name="category-list"),
    path("category/create/", views.category_create, name="category-create"),
    path("category/<int:category_id>/edit/", views.category_edit, name="category-edit"),
    path("category/<int:category_id>/delete/", views.category_delete, name="category-delete")
]
