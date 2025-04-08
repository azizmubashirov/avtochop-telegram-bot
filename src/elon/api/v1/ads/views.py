import json
import requests
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from elon.api.v1.ads.serializers import AdFavouriteSerializer
from elon.ads.models import AdFavourite, Ad
from elon.api.v1.ads import services
from rest_framework import status
from django.urls import reverse

class AdFavouriteView(GenericAPIView):
    serializer_class = AdFavouriteSerializer

    def get_object(self, *args, **kwargs):
        try:
            object = AdFavourite.objects.get(pk=kwargs.get("pk"))
        except Exception:
            raise NotFound("AdFavourite not found")
        return object
    
    def post(self, request):
        """Elonni sevimliga qo'shish"""
        ad = Ad.objects.filter(id=int(request.GET.get("ad", 0))).first()
        try:
            model = AdFavourite.objects.get(ad_id=int(request.GET.get("ad", 0)), user_id=int(request.GET.get("user", 0)))
            if model.status == 1:
                model.status = -1
                model.save()
                ad.favourite_count -= 1
                ad.save()
                return Response({"status": model.status}, status.HTTP_200_OK)
            else:
                model.status = 1
                model.save()
                ad.favourite_count += 1
                ad.save()
                return Response({"status": model.status}, status.HTTP_200_OK)
        except:
            model = AdFavourite(
                ad_id = int(request.GET.get("ad", 0)), 
                user_id = int(request.GET.get("user", 0)),
                status = 1
            )
            model.save()
            ad.favourite_count += 1
            ad.save()
            return Response({"status": model.status}, status.HTTP_200_OK)
  