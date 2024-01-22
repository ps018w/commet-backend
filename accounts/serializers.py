from rest_framework import serializers
from .models import CustomUser, Calendar, UserDetails, UserEducation, TeachingPreference, BookingSlot
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Calendar, Timeslot, BookingSlot


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


# class AuthUserSerializer(UsersSerializer):
#     class Meta(UsersSerializer.Meta):
#         fields = UsersSerializer.Meta.fields
class AuthUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


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

class TimeslotSerializer(serializers.ModelSerializer):

    class Meta:
        model=Timeslot
        fields = '__all__'


class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSlot
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
