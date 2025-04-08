from django.urls import path
from elon.api.tg.users.views import UsersView, UserLogView


urlpatterns = [
    path('create/', UsersView.as_view(), name='user-list'),
    path('list/', UsersView.as_view(), name='users-list'),
    path('<int:chat_id>/info/', UsersView.as_view(), name='user-by-chat'),
    path('<int:pk>/detail/', UsersView.as_view(), name='user-detail'),
    path('<int:chat_id>/log/', UserLogView.as_view(), name='user-log'),
]
