from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from elon.api.v1.eav.value.serializers import ValueSerializer, AttributeValueSerializer
from elon.eav.models import Value, AttributeValue
from elon.api.v1.eav.value import services
from django.urls import reverse


class ValueView(GenericAPIView):
    serializer_class = ValueSerializer
    queryset = Value.objects.all()

    def get_object(self, *args, **kwargs):

        try:
            value = Value.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('value not found')
        return value

    def post(self, request, *args, **kwargs):
        """ Post attribute value """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_value_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """ Put attribute value """
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_value_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ delete value """
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """ get value list or get value one """
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_value_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_value_list(request), status=status.HTTP_200_OK)


class AttributeValueView(GenericAPIView):
    serializer_class = AttributeValueSerializer
    queryset = AttributeValue.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            attribute_value = AttributeValue.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('attribute value not found')
        return attribute_value

    def post(self, request, *args, **kwargs):
        """ post attribute value"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_attribute_value_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """ put attribute value"""
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_attribute_value_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """ delete attribute value """
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """ get attribute value list or get attribute one """
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_attribute_value_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_attribute_value_list(request), status=status.HTTP_200_OK)
