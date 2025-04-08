from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from elon.geo.serializers import RegionSerializer, DistrictSerializer
from elon.geo.models import Region, District
from elon.geo import services
from elon.geo.permissions import RegionAndDistrictPermission
from django.urls import reverse


class RegionView(GenericAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    permission_classes = (RegionAndDistrictPermission, )

    def get_object(self, *args, **kwargs):
        try:
            subject = Region.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('Region not found')
        return subject

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_region_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_region_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            if request.get_full_path() == reverse('region-children', kwargs=kwargs):
                result = services.get_region_with_children(request, kwargs["pk"])
            else:
                result = services.get_region_one(request, kwargs['pk'])
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = services.get_region_list(request)
            return Response(result, status=status.HTTP_200_OK)


class DistrictView(GenericAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()
    permission_classes = (RegionAndDistrictPermission, )

    def get_object(self, *args, **kwargs):
        try:
            subject = District.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('District not found')
        return subject

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_district_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_district_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            result = services.get_district_one(request, kwargs['pk'])
            return Response(result, status=status.HTTP_200_OK)
        else:
            result = services.get_district_list(request)
            return Response(result, status=status.HTTP_200_OK)
