from eelon.base.serializers import (
    TitleSerializer, LabelSerializer, UnitSerializer, ValidationSerializer,
    MessageSerializer, AttributePropertiesSerializer, HelpSerializer, ConfigSerializer
)
from eelon.eav.models import (
    Category, InputType, Entity, CategoryEntity, Attribute, EntityAttribute,
    Value, AttributeValue
)
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    title = TitleSerializer(required=True)
    # slug = serializers.CharField(max_length=255, allow_blank=False, allow_null=False)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('id', 'created_at')

    # def create(self, validated_data):
    #     category = Category(**validated_data)
    #     category.save()
    #     return category


class InputTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputType
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class EntitySerializer(serializers.ModelSerializer):
    title = TitleSerializer(required=True)
    config = ConfigSerializer(required=True)

    class Meta:
        model = Entity
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class CategoryEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryEntity
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class AttributeSerializer(serializers.ModelSerializer):
    properties = AttributePropertiesSerializer(required=True)

    class Meta:
        model = Attribute
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class EntityAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityAttribute
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class ValueSerializer(serializers.ModelSerializer):
    label = LabelSerializer(required=True)

    class Meta:
        model = Value
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
