from django.urls import path
from .views import UserModelList, SignUpView, LoginAPIView

urlpatterns = [
    path('user/', UserModelList.as_view(), name='user'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),

]