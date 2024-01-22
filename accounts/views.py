from rest_framework.views import APIView
from rest_framework import status
from .models import CustomUser, Calendar
from .serializers import UsersSerializer, AuthUserSerializer, CalendarSerializer, BookingSlot, BookingSlotSerializer
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login

from rest_framework.authentication import SessionAuthentication
from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from accounts.services import create_slot, booked_teaching_slot


class UserModelList(APIView):
    def get(self, request):
        my_models = CustomUser.objects.all()
        serializer = UsersSerializer(my_models, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    # queryset = CustomUser.objects.all()
    #serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(responses={200: AuthUserSerializer()}, request_body=AuthUserSerializer)
    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

    # @swagger_auto_schema(responses={200: AuthUserSerializer()})
    def post(self, request, format=None):
        serializer = AuthUserSerializer(data=request.data)
        print(request)
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalendarCreateView(APIView):
    queryset = Calendar.objects.all()

    # serializer_class = CalendarSerializer(data=queryset)
    @swagger_auto_schema(responses={200: CalendarSerializer(many=True)})
    def get(self, request, format=None):
        user = CustomUser.objects.get(email=request.data['email'])
        calendar = Calendar.objects.filter(user=user)
        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CalendarSerializer(data=request.data)

        data = create_slot(request)  # freq, user, start_time,days_of_week)
        # print(slot_data)
        if data:
            return Response({'message': 'Schedules created successfully.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Errors'}, status=status.HTTP_400_BAD_REQUEST)


class DeleteTutorSlot(APIView):
    def delete(self, request):
        try:
            day_of_week = request.data.get('days_of_week')
            email = request.data.get('email')
            user = CustomUser.objects.get(email=email)
            schedule_date = request.data.get('schedule_date')

            if not day_of_week:
                return Response({'error': 'Day of the week is required.'}, status=status.HTTP_400_BAD_REQUEST)
            elif day_of_week and not schedule_date:
                Calendar.objects.filter(user=user.id, days_of_week=day_of_week).delete()
                return Response({'message': f'Schedules for ALL {day_of_week} deleted successfully.'},
                                status=status.HTTP_200_OK)
            elif day_of_week and schedule_date:

                Calendar.objects.filter(user=user.id, days_of_week=day_of_week, schedule_date=schedule_date).delete()
                return Response({'message': f'Schedules for {day_of_week}: {schedule_date} deleted successfully.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({"message": "No schedule found to deleted"}, status=status.HTTP_404_NOT_FOUND)


        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingSlot(APIView):

    permission_classes = [AllowAny]


    @swagger_auto_schema(request_body=BookingSlotSerializer)
    def post(self, request):

        data = request.data

        booked_slot = booked_teaching_slot(data,request=request)

        return Response({'message': 'Schedules booked successfully.'}, status=status.HTTP_200_OK)








        pass




