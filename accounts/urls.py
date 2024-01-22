from django.urls import path
from .views import UserModelList, SignUpView, LoginAPIView, CalendarCreateView,\
    DeleteTutorSlot,BookingSlot,UserDetailsApi, UserEducationAPI, TeachingPreferenceAPI

urlpatterns = [
    path('user/', UserModelList.as_view(), name='user'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('tutor-time-slot/', CalendarCreateView.as_view(), name='time-slot-create'),
    path('tutor-time-slot_delete/', DeleteTutorSlot.as_view(), name='time-slot-delete'),
    path('bookings/', BookingSlot.as_view(), name='booking_slot'),
    path('UserDetailsApi/', UserDetailsApi.as_view(), name='userdetailsapi'),
    path('UserEducationAPI/', UserEducationAPI.as_view(), name='Usereducationapi'),
    path('TeachingPreferenceAPI/', TeachingPreferenceAPI.as_view(), name='teachingpreferenceapi'),
    path('logout/', UserDetailsApi.as_view(), name='userdetailsapi'),
]