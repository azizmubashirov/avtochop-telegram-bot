from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotFound
from . import services
from .serializers import UsersSerializer, UserLogSerializer
from .models import User, Log


class UsersView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UsersSerializer

    def get_object(self, *args, **kwargs):
        try:
            if 'pk' in kwargs and kwargs['pk']:
                product = User.objects.get(pk=kwargs['pk'])
            elif 'chat_id' in kwargs and kwargs['chat_id']:
                product = User.objects.get(chat_id=kwargs['chat_id'])
            else:
                raise NotFound('Not found User')
        except Exception as e:
            raise NotFound('Not found User')
        return product

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_user_by_pk(request, data.id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_user_by_pk(request, data.id)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs and kwargs['pk']:
            result = services.one_user_by_pk(request, pk=kwargs['pk'])
        elif 'chat_id' in kwargs and kwargs['chat_id']:
            result = services.one_user_by_chat_id(request, chat_id=kwargs['chat_id'])
        else:
            result = services.list_product(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')


class UserLogView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLogSerializer

    def get_object(self, *args, **kwargs):
        try:
            product = Log.objects.get(user_id=kwargs['chat_id'])
        except Exception as e:
            raise NotFound('not found product')
        return product

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        root = serializer.save()
        result = services.one_log(request, user_id=root.user_id)
        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        root = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=root, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = services.one_log(request, user_id=data.user_id)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def get(self, request, *args, **kwargs):
        if 'chat_id' in kwargs and kwargs['chat_id']:
            result = services.one_log(request, user_id=kwargs['chat_id'])
        else:
            result = None
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')