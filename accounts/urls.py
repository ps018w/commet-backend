from django.urls import path
from .views import UserModelList

urlpatterns = [
    path('user/', UserModelList.as_view(), name='user'),
]