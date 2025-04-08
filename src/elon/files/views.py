from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from elon.files.serializers import FileSerializer
from rest_framework.parsers import MultiPartParser
from elon.files.models import File
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class FileView(GenericAPIView):

    serializer_class = FileSerializer
    parser_classes = [MultiPartParser]

    def get(self, request, *args, **kwargs):
        if kwargs.get("pk"):
            file = File.objects.get(pk=kwargs.get("pk"))
            short_report = open(BASE_DIR / "media" / file.file.path, 'rb')
            name, extension = os.path.splitext(file.file.name)
            response = HttpResponse(FileWrapper(short_report), content_type=f'image/{str(extension).strip(".")}')
            return response
        else:
            raise NotFound("File not found")

    def post(self, request):
        serializer = FileSerializer(data=[{"file": file} for file in request.data.getlist("file")], many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {}
        for file in serializer.data:
            data = {
                'file_url': file.get('file_url'),
                'versatil_url': file.get('versatil_url'),
            }
        print(data)
        return Response({'data': data})
        # return Response([file.get("file_url") for file in serializer.data])