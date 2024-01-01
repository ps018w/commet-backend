
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Calendar
from .serializers import UsersSerializer,AuthUserSerializer, CalendarSerializer
from rest_framework.permissions import AllowAny
#from rest_framework_api_key.per

from django.contrib.auth import authenticate, login

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

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
    # serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):


        return {
            'request':self.request,
            'format':self.format_kwarg,
            'view':self
        }

    def post(self, request, format=None):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny ]

    def get_serializer_context(self):


        return {
            'request':self.request,
            'format':self.format_kwarg,
            'view':self
        }

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


from rest_framework import generics
from rest_framework.response import Response
#from .models import Meeting, RecurringMeeting
#from .serializers import C, RecurringMeetingSerializer
from dateutil import rrule
from datetime import datetime

class CalendarCreateView(generics.ListCreateAPIView):
    queryset = Calendar.objects.all()

    serializer_class = CalendarSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        recurring_meeting = serializer.save()

        if recurring_meeting.recurrence_pattern == 'daily':
            recurrence_rule = rrule.DAILY
        elif recurring_meeting.recurrence_pattern == 'weekly':
            recurrence_rule = rrule.WEEKLY
        else:
            # Handle other recurrence patterns as needed
            recurrence_rule = rrule.DAILY

        meetings = list(
            rrule.rrule(
                recurrence_rule,
                dtstart=recurring_meeting.meeting.date_time,
                until=recurring_meeting.recurrence_end_date
            )
        )

        for meeting_time in meetings:
            Calendar.objects.create(
                title=recurring_meeting.meeting.title,
                date_time=meeting_time,
                description=recurring_meeting.meeting.description
            )
