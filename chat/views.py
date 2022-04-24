from django.shortcuts import render
from accounts.models import User
from .models import ChatModel
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class index(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user_obj = User.objects.all()
            for x in user_obj:
                if request.user.id > x.id:
                    thread_name = f'chat_{request.user.id}-{x.id}'
                else:
                    thread_name = f'chat_{x.id}-{request.user.id}'
                message_obj = ChatModel.objects.filter(thread_name=thread_name)
                if message_obj:
                    users = User.objects.exclude(username=request.user.username).filter(username=x.username)
                    return Response({'users':users},status=status.HTTP_200_OK)
                else:
                    return Response({'msg':"No chat"},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'msg':"No chat"},status=status.HTTP_204_NO_CONTENT)


class chatPage(APIView):
    permission_classes = [IsAuthenticated]


    def chatPage(self, request, username, format=None):
        try:
            user_obj = User.objects.get(username=username)
            users = User.objects.all()
            for x in users:
                if request.user.id > x.id:
                    thread_name = f'chat_{request.user.id}-{x.id}'
                else:
                    thread_name = f'chat_{x.id}-{request.user.id}'
                message_obj = ChatModel.objects.filter(thread_name=thread_name)
                if message_obj:
                    users = User.objects.exclude(username=request.user.username).filter(username=x.username)
                    paginator = PageNumberPagination()
                    result_page = paginator.paginate_queryset(message_obj, request)
                    return Response({'users':users, 'user':user_obj, 'messages':result_page}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg':"No chat"},status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response("Exception: Data not found")
