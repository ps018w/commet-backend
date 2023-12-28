
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UsersSerializer

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
