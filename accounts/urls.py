from django.urls import path
from .views import UserModelList, SignUpView, LoginAPIView, CalendarCreateView

urlpatterns = [
    path('user/', UserModelList.as_view(), name='user'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('meetings/', CalendarCreateView.as_view(), name='meeting-list-create'),

]