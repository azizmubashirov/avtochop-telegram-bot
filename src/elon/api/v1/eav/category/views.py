from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from elon.api.v1.eav.category.serializers import CategorySerializer
from elon.eav.models import Category
from elon.api.v1.eav.category import services
from django.urls import reverse

class CategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            subject = Category.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('category not found')
        return subject

    def post(self, request, *args, **kwargs):
        """ Category create """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_category_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """ category edit """
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_category_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ category delete """
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            result = services.get_category_one(request, pk=kwargs['pk'])
            return Response(result, status=status.HTTP_200_OK)
        elif 'category_slug' in kwargs and kwargs['category_slug']:
            """ cateogory slug bilan category haqida malumot olib keladi """
            result = services.get_category_one(request, slug=kwargs['category_slug'])
            return Response(result, status=status.HTTP_200_OK)
        else:
            if request.path == reverse('api:category-main', kwargs=kwargs):
                """ get Category list """
                result = services.get_category_list(request, action="menu")
            elif request.path == reverse('api:category-sale-list', kwargs=kwargs):
                """ get Cateogory sale list """
                result = services.get_category_sale_list(request, action="sale")
            else:
                """ get Category list """
                result = services.get_category_list(request)
            return Response(result, status=status.HTTP_200_OK)

class CategoryStepsView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        """ get category steps list """
        result = services.get_category_steps(request, kwargs['category_id'])
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')