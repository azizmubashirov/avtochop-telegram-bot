from django.urls import include, path
from elon.dashboard.users import views


urlpatterns = [
    path("users/list/", views.users_list, name="users-list")
]
