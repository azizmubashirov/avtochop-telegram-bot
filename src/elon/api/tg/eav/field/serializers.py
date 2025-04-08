from elon.base.serializers import LabelSerializer
from elon.eav.models import Marka, Model, Positsion
from rest_framework import serializers


class MarkaSerializer(serializers.ModelSerializer):
    label = LabelSerializer(required=True)

    class Meta:
        model = Marka
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class MadelValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class PositsionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Positsion
        fields = "__all__"
        read_only_fields = ('id', 'created_at')