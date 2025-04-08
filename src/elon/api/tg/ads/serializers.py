from rest_framework import serializers
from eelon.ads.models import Ad, AdComment
from eelon.api.tg.eav.category.services import get_category_steps


class ContactSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, allow_blank=False, allow_null=True)


class LocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(max_digits=13, decimal_places=10, required=True, allow_null=False)
    longitude = serializers.DecimalField(max_digits=13, decimal_places=10, required=True, allow_null=False)


class AdSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    location = LocationSerializer()

    def validate(self, attrs):
        if attrs.get("properties"):
            try:
                category = attrs.get("category")
                title = category.title_auto.get("title_auto_uz")
                fields = get_category_steps(None, category.id)['fields']
                for field in fields:
                    properties = attrs.get("properties")
                    if field['properties']['validation']['rule'] == 'required':
                        value = properties.get(f"{field['slug']}", None)
                        if value:
                            if field['is_title'] and field['input_type'] == "select":
                                if str(value).isdigit():
                                    for pro in field['properties']['values']:
                                        if int(value) == int(pro['value']):
                                            title += " " + pro.get("label", {}).get("label_uz")
                                            break
                                else:
                                    title += " " + value[:20]
                            elif field['is_title'] and field['input_type'] == "text":
                                title += " " + value[:20]
                        else:
                            raise serializers.ValidationError("Value is empty!")
                attrs['title'] = title
            except Exception as e:
                print("Cannot validate data:", e)
                raise serializers.ValidationError("Cannot validate data:", e)
        return attrs

    def create(self, validated_data):
        validated_data['location'] = {
            "latitude": float(validated_data['location'].get("latitude")),
            "longitude": float(validated_data['location'].get("longitude"))
        }
        model = Ad(**validated_data)
        model.save()
        return model
    
    def update(self, instance, validated_data):
        instance.message_id = validated_data.get('message_id')
        instance.chat_id = validated_data.get('chat_id')
        instance.status = validated_data.get('status')
        instance.save()
        return instance

    class Meta:
        model = Ad
        fields = "__all__"


class AdCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdComment
        fields = "__all__"
