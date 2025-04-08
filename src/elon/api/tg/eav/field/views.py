from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from elon.api.tg.eav.field.serializers import *
from elon.eav.models import Category
from elon.api.tg.eav.field import services
from django.urls import reverse



class FieldView(GenericAPIView):
    serializer_class = MarkaSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk") and request.path == reverse('tg:marka-view', kwargs=kwargs):
            category = Category.objects.get(pk=int(kwargs.get("pk")))
            return Response(services.get_marka_category(request, category.marka), status=status.HTTP_200_OK)
        elif kwargs.get("category_slug") and request.path == reverse('tg:marka-view-slug', kwargs=kwargs):
            category = Category.objects.get(slug=kwargs.get("category_slug"))
            return Response(services.get_marka_category(request, category.marka), status=status.HTTP_200_OK)
        elif kwargs.get('pk') and request.path == reverse('tg:madel-view', kwargs=kwargs):
            return Response(services.get_model(request, marka_id = kwargs.get('pk')), status=status.HTTP_200_OK)
        elif kwargs.get('marka_slug') and request.path == reverse('tg:madel-view-slug', kwargs=kwargs):
            return Response(services.get_model(request, marka_slug = kwargs.get('marka_slug')), status=status.HTTP_200_OK)

        elif kwargs.get('pk') and request.path == reverse('tg:positsion-view', kwargs=kwargs):
            return Response(services.get_positsion(request, model_id = kwargs.get('pk')), status=status.HTTP_200_OK)
        elif kwargs.get('madel_slug') and request.path == reverse('tg:positsion-view-slug', kwargs=kwargs):
            return Response(services.get_positsion(request, madel_slug = kwargs.get('madel_slug')), status=status.HTTP_200_OK)


        elif kwargs.get('mark_id') and request.path == reverse('tg:marka-info', kwargs=kwargs):
            return Response(services.get_mark_value_one(request, kwargs.get('mark_id')), status=status.HTTP_200_OK)
        elif kwargs.get('madel_id') and request.path == reverse('tg:madel-info', kwargs=kwargs):
            return Response(services.get_madel_value_one(request, kwargs.get('madel_id')), status=status.HTTP_200_OK)
        elif kwargs.get('pos_id') and request.path == reverse('tg:positsion-info', kwargs=kwargs):
            return Response(services.get_positsion_value_one(request, kwargs.get('pos_id')), status=status.HTTP_200_OK)


