from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from eelon.eav.serializers import (
    CategorySerializer, InputTypeSerializer, EntitySerializer, CategoryEntitySerializer,
    AttributeSerializer, EntityAttributeSerializer, ValueSerializer, AttributeValueSerializer
)
from eelon.eav.models import (
    Category, InputType, Entity, CategoryEntity, Attribute, EntityAttribute, Value, AttributeValue
)
from eelon.eav import services
from .permissions import CategoryPermission
from django.urls import reverse
from eelon.eav.renderer import CustomJSONRenderer


class CategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (CategoryPermission, )
    parser_classes = (CustomJSONRenderer, )

    def get_object(self, *args, **kwargs):
        try:
            subject = Category.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('category not found')
        return subject

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_category_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_category_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            if request.get_full_path() == reverse('tg-category-children', kwargs=kwargs):
                result = services.get_category_list(request, action="children", category_id=kwargs["pk"])
            else:
                result = services.get_category_one(request, kwargs['pk'])
            return Response(result, status=status.HTTP_200_OK)
        else:
            if request.get_full_path() == reverse('tg-category-create', kwargs=kwargs):
                result = services.get_category_list(request, action="menu")
            else:
                result = services.get_category_list(request)
            return Response(result, status=status.HTTP_200_OK)


class InputTypeView(GenericAPIView):
    serializer_class = InputTypeSerializer
    queryset = InputType.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            subject = InputType.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('input type not found')
        return subject

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_input_type_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_input_type_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_input_type_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_input_type_list(request), status=status.HTTP_200_OK)


class EntityView(GenericAPIView):
    serializer_class = EntitySerializer
    queryset = Entity.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            subject = Entity.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('entity not found')
        return subject

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_entity_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_entity_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_entity_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_entity_list(request), status=status.HTTP_200_OK)


class CategoryEntityView(GenericAPIView):
    serializer_class = CategoryEntitySerializer
    queryset = CategoryEntity.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            subject = CategoryEntity.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('category entity not found')
        return subject

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_category_entity_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_category_entity_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_category_entity_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_category_entity_list(request), status=status.HTTP_200_OK)


class AttributeView(GenericAPIView):
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            attribute = Attribute.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('attribute not found')
        return attribute

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_attribute_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_attribute_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_attribute_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_attribute_list(request), status=status.HTTP_200_OK)


class EntityAttributeView(GenericAPIView):
    serializer_class = EntityAttributeSerializer
    queryset = EntityAttribute.objects.all()

    def get_object(self, *args, **kwargs):
        try:
            attribute = EntityAttribute.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('entity attribute not found')
        return attribute

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_entity_attribute_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_entity_attribute_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_entity_attribute_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_entity_attribute_list(request), status=status.HTTP_200_OK)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_value_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_value_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_attribute_value_one(request, data.pk), status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(services.get_attribute_value_one(request, data.pk), status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object(*args, **kwargs)
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs["pk"]:
            return Response(services.get_attribute_value_one(request, kwargs['pk']), status=status.HTTP_200_OK)
        else:
            return Response(services.get_attribute_value_list(request), status=status.HTTP_200_OK)


class CategoryStepsView(GenericAPIView):

    renderer_classes = [CustomJSONRenderer]

    def get(self, request, *args, **kwargs):
        result = services.get_category_steps(request, kwargs['category_id'])
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')
