from rest_framework import serializers


class TitleSerializer(serializers.Serializer):
    title_uz = serializers.CharField(allow_blank=False, max_length=300, required=True)
    title_ru = serializers.CharField(allow_blank=False, max_length=300, required=True)


class LabelSerializer(serializers.Serializer):
    label_uz = serializers.CharField(allow_blank=False, max_length=300, required=True)
    label_ru = serializers.CharField(allow_blank=False, max_length=300, required=True)


class HelpSerializer(serializers.Serializer):
    help_uz = serializers.CharField(allow_blank=True, max_length=300, required=True)
    help_ru = serializers.CharField(allow_blank=True, max_length=300, required=True)


class MessageSerializer(serializers.Serializer):
    message_uz = serializers.CharField(allow_blank=False, max_length=300, required=True)
    message_ru = serializers.CharField(allow_blank=False, max_length=300, required=True)


class UnitSerializer(serializers.Serializer):
    unit_uz = serializers.CharField(allow_blank=True, max_length=300, required=True)
    unit_ru = serializers.CharField(allow_blank=True, max_length=300, required=True)


class ValidationSerializer(serializers.Serializer):
    rule = serializers.CharField(allow_blank=False, max_length=300, required=True)
    min = serializers.IntegerField(allow_null=False, required=True)
    max = serializers.IntegerField(allow_null=False, required=True)
    message = MessageSerializer(required=True)


class AttributePropertiesSerializer(serializers.Serializer):
    dataType = serializers.CharField(allow_blank=False, max_length=255, required=True)
    label = LabelSerializer(required=True)
    help = HelpSerializer(required=True)
    validation = ValidationSerializer(required=True)
    unit = UnitSerializer(required=True)
    multiple = serializers.BooleanField(allow_null=True, required=True)


class ConfigSerializer(serializers.Serializer):
    show_label = serializers.BooleanField(required=True)
