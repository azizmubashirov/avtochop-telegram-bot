from django.urls import path

from eelon.users.views import UsersView, UserLogView


urlpatterns = [
    path('user/', UsersView.as_view(), name='user-list'),
    path('user/<int:pk>/', UsersView.as_view(), name='user-by-pk'),
    path('user/<int:chat_id>/tg/', UsersView.as_view(), name='user-by-chat'),
    path('log/<int:chat_id>/tg/', UserLogView.as_view(), name='user-log'),
]
