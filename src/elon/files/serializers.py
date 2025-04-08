from django.conf import settings
from rest_framework import serializers
import ssl
from elon.files.models import File as ModelFile


MEDIA_URL = getattr(settings, "MEDIA_HOST")
ssl._create_default_https_context = ssl._create_unverified_context

class FileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField('get_file_url')
    versatil_url = serializers.SerializerMethodField("get_versatil_url")

    def get_file_url(self, obj):
        return f"{MEDIA_URL}{obj.file.url}"

    def get_versatil_url(self, obj):
        return f"{MEDIA_URL}{obj.file.thumbnail['195x144'].url}"

    class Meta:
        model = ModelFile
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

