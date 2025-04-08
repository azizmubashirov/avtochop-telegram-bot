from django.urls import path

from elon.api.v1.users.views import UsersView, UsersSearchView


urlpatterns = [
    path('list/', UsersView.as_view(), name='user-list'),
    path('search/', UsersSearchView.as_view(), name='user-search'),
]
