import imp
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import AddCategorySerializer, CategorySerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from .models import Categories

# Create your views here.


class AddCategory(APIView):
    serializer_class = AddCategorySerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, format=None):
        try:
            if self.request.user.is_admin:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Category(APIView):
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminUser]

    def get_object(self, id):
        try:
            data = Categories.objects.get(id=id)
            return data
        except:
            raise Http404

    def get(self, request, id, format=None):
        try:
            if self.request.user.is_admin:
                serializer = self.serializer_class(self.get_object(id))
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        try:
            if self.request.user.is_admin:
                data = self.get_object(id)
                serializer = self.serializer_class(data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request, id, format=None):
        try:
            if self.request.user.is_admin:
                data = self.get_object(id)
                data.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    def get(self, request, format=None):
        try:
            if self.request.user.is_admin:
                data = Categories.objects.all()
                serilaizer = CategorySerializer(data, many=True)
                serialized_data = serilaizer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            raise Http404

    