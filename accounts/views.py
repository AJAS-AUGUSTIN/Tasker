from inspect import stack
from logging import exception
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, WorkerSerializer
from rest_framework_simplejwt.tokens import RefreshToken


from accounts import serializers
# Create your views here.


class UserRegistration(APIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    def post(self, request, format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_OK)
        except exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WorkerRegistration(APIView):
    serializer_class = WorkerSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print("worker",serializer)
        if serializer.is_valid():
            print("11111111111111")
            user = serializer.save()
            print("2222222222222222")
            refresh = RefreshToken.for_worker(user)

            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        print("Serializer not valid")
        return Response(status=status.HTTP_400_BAD_REQUEST)