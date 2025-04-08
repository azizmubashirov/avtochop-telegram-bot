from rest_framework import serializers
from eelon.ads.models import Ad
from eelon.eav.models import Category
from eelon.ads.services import get_category_fields
import json
from decimal import Decimal
import logging

logger = logging.getLogger('api')


class ContactSerializer(serializers.Serializer):
    # email = serializers.EmailField(max_length=200, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(max_length=13, allow_blank=False, allow_null=True)


class LocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=13, decimal_places=10, required=True, allow_null=False)
    longitude = serializers.DecimalField(max_digits=13, decimal_places=10, required=True, allow_null=False)


class AdSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(required=True)
    location = LocationSerializer(required=True)

    def validate(self, attrs):
        try:
            category = attrs.get("category")
            fields = get_category_fields(category.id)
            for field in fields:
                properties = attrs.get("properties")
                value = properties.get(f"{field['slug']}", None)
                logger.error("{} - {}".format(field['slug'], value))
                if value:
                    if field['data_type'] == 'integer':
                        if not isinstance(value, int):
                            raise serializers.ValidationError("Value type error!")
                    elif field['data_type'] == 'string':
                        if not isinstance(value, str):
                            raise serializers.ValidationError("Value type error!")
                    else:
                        raise serializers.ValidationError("Value type not found!")
                else:
                    raise serializers.ValidationError("Value is empty!")
        except Exception as e:
            logger.error("Error: {}".format(e))
            raise serializers.ValidationError("Cannot validate data")
        return attrs

    class Meta:
        model = Ad
        fields = "__all__"

    def create(self, validated_data):
        validated_data['location'] = {
            "latitude": float(validated_data['location'].get("latitude")),
            "longitude": float(validated_data['location'].get("longitude"))
        }
        model = Ad(**validated_data)
        model.save()
        return model

