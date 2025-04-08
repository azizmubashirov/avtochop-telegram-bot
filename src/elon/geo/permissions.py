from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class RegionAndDistrictPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return IsAdminUser().has_permission(request, view)
