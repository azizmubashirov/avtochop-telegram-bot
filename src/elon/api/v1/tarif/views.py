from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from django.urls import reverse
from . import services
from elon.ads.models import Ad


class TarifView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        """ get region list"""
        ad_id = int(request.GET.get("ad_id"))
        ad = Ad.objects.get(pk=ad_id)
        category_id = ad.category.id
        services_alias = ["top", "start", "vip"]
        result = services.get_services(services_alias, category_id)
        return Response(result, status=status.HTTP_200_OK)