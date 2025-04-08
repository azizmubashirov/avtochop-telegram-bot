
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from elon.api.v1.users import services
from elon.api.v1.users.serializers import UsersSerializer


class UsersView(GenericAPIView):
    serializer_class = UsersSerializer

    def get(self, request, *args, **kwargs):
        result = services.list_product(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

class UsersSearchView(GenericAPIView):
    def get(self, request):
        result = services.list_search(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')