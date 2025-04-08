from rest_framework import permissions
from rest_framework.permissions import IsAdminUser


class OnlyGetAndCreatePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET' or request.method == 'POST':
            return True
        else:
            return IsAdminUser().has_permission(request, view)
