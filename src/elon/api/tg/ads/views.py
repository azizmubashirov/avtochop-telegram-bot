import imp
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from eelon.api.tg.ads.serializers import AdSerializer, AdCommentSerializer
from eelon.ads.models import Ad, Category
from eelon.api.tg.ads import services
from rest_framework import status
from django.urls import reverse
from telegram import bot
from django.conf import settings
from django.utils import timezone


class AdView(GenericAPIView):

    serializer_class = AdSerializer
    categories = []

    def get_object(self, *args, **kwargs):
        try:
            object = Ad.objects.get(pk=kwargs.get("pk"))
        except Exception:
            raise NotFound("Ad not found")
        return object

    def get_category_children(self, children):
        for child in children:
            children = child.get_children()
            if children:
                self.get_category_children(children)
            else:
                self.categories.append(child.id)

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            return Response(services.get_ad_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        elif kwargs.get("category_id") and request.path == reverse('tg:ads-by-categories', kwargs=kwargs):
            self.categories = []
            children = Category.objects.get(pk=kwargs.get("category_id", 0)).get_children()
            self.get_category_children(children)
            return Response(services.get_ad_list_by_categories(request, self.categories), status=status.HTTP_200_OK)
        else:
            return Response(services.get_ad_list(request), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        model = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=model, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            model = self.get_object(*args, **kwargs)
            model.status = 6
            model.deleted_by = model.user
            model.deleted_at = timezone.now()
            model.save()
            return Response({"deactivated": True})
        except:
            return Response({"deactivated": False})


class AdCommentView(GenericAPIView):
    serializer_class = AdCommentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

