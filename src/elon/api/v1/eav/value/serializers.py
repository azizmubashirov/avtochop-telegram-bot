from elon.base.serializers import LabelSerializer
from elon.eav.models import Value, AttributeValue, Attribute
from rest_framework import serializers


class ValueSerializer(serializers.ModelSerializer):
    label = LabelSerializer(required=True)

    class Meta:
        model = Value
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class AttributeValueSerializer2(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class AttributeValueSerializer(serializers.Serializer):
    attribute = serializers.ModelField(model_field=Attribute()._meta.get_field('id'))
    values = serializers.ListField(
        child=serializers.ModelField(model_field=Value()._meta.get_field('id')), required=True
    )

    def create(self, validated_data):
        try:
            attribute = validated_data.pop("attribute")
            values = validated_data.pop("values")

            for index, value in enumerate(values):
                attribute_value_model = AttributeValue.objects.filter(attribute_id=attribute, value_id=value).exists()
                if not attribute_value_model:
                    attribute_value_model = AttributeValue(
                        eattribute_id=attribute, value_id=value, sorting=index + 1
                    )
                else:
                    attribute_value_model = AttributeValue.objects.get(attribute_id=attribute, value_id=value)
                    attribute_value_model.sorting = index + 1
                attribute_value_model.save()
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def update(self, instance, validated_data):
        try:
            attribute = validated_data.pop("attribute")
            values = validated_data.pop("values")

            for index, value in enumerate(values):
                attribute_value_model = AttributeValue.objects.filter(attribute_id=attribute, value_id=value).exists()
                if not attribute_value_model:
                    attribute_value_model = AttributeValue(
                        eattribute_id=attribute, value_id=value, sorting=index + 1
                    )
                else:
                    attribute_value_model = AttributeValue.objects.get(attribute_id=attribute, value_id=value)
                    attribute_value_model.sorting = index + 1
                attribute_value_model.save()
            return True
        except Exception as e:
            print("Error:", e)
            return False