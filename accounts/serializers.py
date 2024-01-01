from rest_framework import serializers
from .models import CustomUser, Calendar


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "full_name",
            "password",
            "time_zone",
            "user_type"
        ]
        extra_kwargs = {'password': {'write_only': True}}


class AuthUserSerializer(UsersSerializer):
    class Meta(UsersSerializer.Meta):
        fields = UsersSerializer.Meta.fields


class CalendarSerializer(serializers.ModelSerializer):


    class Meta:
        model = Calendar
        fields = '__all__'
