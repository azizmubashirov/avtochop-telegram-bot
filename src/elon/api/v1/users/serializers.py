from rest_framework import serializers
from elon.users.models import User, Log


class UsersSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        root = User.objects.create_telegram_user(
            chat_id=validated_data.get("chat_id"), tg_username=validated_data.get("tg_username"),
            tg_firstname=validated_data.get("tg_firstname"), tg_lastname=validated_data.get("tg_lastname"),
            is_telegram=validated_data.get("is_telegram")
        )
        return root

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ("id", "tab_number", "password", )


class UserLogSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        root = Log(**validated_data)
        root.save()
        return root

    class Meta:
        model = Log
        fields = '__all__'
