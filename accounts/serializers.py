from rest_framework import serializers
from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "full_name",
            "password",
            # "timezone",
        ]
        extra_kwargs = {'password': {'write_only': True}}


class AuthUserSerializer(UsersSerializer):
    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields
