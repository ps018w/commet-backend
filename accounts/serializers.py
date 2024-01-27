from rest_framework import serializers
from .models import CustomUser, Calendar, UserDetails, UserEducation, TeachingPreference, BookingSlot
from rest_framework_simplejwt.tokens import RefreshToken
import datetime


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "full_name",
            "password",
            "time_zone",
            "user_type",
            "password"
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        full_name = validated_data['full_name']
        email = validated_data['email']
        password = validated_data['password']
        time_zone = validated_data['time_zone']
        user_type = validated_data['user_type']
        user_obj = CustomUser(
            full_name=full_name,
            email=email,
            time_zone=time_zone,
            user_type=user_type
        )
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


# class AuthUserSerializer(UsersSerializer):
#     class Meta(UsersSerializer.Meta):
#         fields = UsersSerializer.Meta.fields
class AuthUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password','full_name','user_type','time_zone']


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')

    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ['email', 'token', 'full_name', 'time_zone', 'user_type']

    def get_token(self, obj):
        user = CustomUser.objects.get(email=obj.email)
        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return token


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        # fields = '__all__'
        exclude = ['user', 'phone_number']


class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        exclude = ['user']


class TeachingPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeachingPreference
        exclude = ['user']


class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSlot
        fields = '__all__'


def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")


def check_expiry_year(value):
    today = datetime.datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")


def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")


def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")


class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(max_length=150, required=True, validators=[check_expiry_month], )
    expiry_year = serializers.CharField(max_length=150, required=True, validators=[check_expiry_year], )
    cvc = serializers.CharField(max_length=150, required=True, validators=[check_cvc], )
