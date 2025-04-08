from elon.base.serializers import TitleSerializer
from elon.eav.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    title = TitleSerializer(required=True)
    slug = serializers.SlugField(allow_null=True, allow_blank=True)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ('id', 'created_at')

