from urllib import request
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AppliedJobSerializer, ApplyJobSerializer, ViewAllJobsSerializer, UpdateWorkerSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ApplyJob
from user.models import Job
from user.serializers import JobSerializer, WorkerViewSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
from accounts.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class ApplyJobs(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ApplyJobSerializer

    def post(self, request, format=None):
        if self.request.user.is_worker:
            applied_jobs = ApplyJob.objects.filter(
                worker=request.user, job=request.POST['job'])
            if applied_jobs:
                return Response({'msg': "Already Applied"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.serializer_class(
                    data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class JobItem(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get_object(self, id):
        try:
            data = Job.objects.get(id=id)
            self.check_object_permissions(self.request, data)
            return data
        except:
            return Response({"msg": "No job found"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id, format=None):
        try:
            serializer = self.serializer_class(self.get_object(id))
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except:
            return Response({"msg": "No job found"}, status=status.HTTP_400_BAD_REQUEST)


class ViewAllJobs(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination

    def get(self, request, format=None):
        jobs = Job.objects.all()
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(jobs, request)
        serializer = ViewAllJobsSerializer(result_page, many=True, context={'request':request})
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class AppliedJobs(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if self.request.user.is_worker:
            jobs = ApplyJob.objects.filter(worker=request.user)
            serializer = AppliedJobSerializer(jobs, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Not a worker"}, status=status.HTTP_401_UNAUTHORIZED)


class ApprovedJobs(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if self.request.user.is_worker:
            jobs = ApplyJob.objects.filter(worker=request.user, confirmed=True)
            serializer = AppliedJobSerializer(jobs, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Not a worker"}, status=status.HTTP_401_UNAUTHORIZED)


class SearchJobs(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'category__title',
                     'minimum_wage', 'city', 'landmark', 'requirements']
    filterset_fields = ['title', 'category', 'minimum_wage', 'city', 'user']



class SearchUser(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_user=True)
    serializer_class = WorkerViewSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name',
                     'email', 'phone_number']
    ordering_fields = ['username', 'email']
    ordering = ['username']


class UpdateProfileView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateWorkerSerializer


    def put(self, request, id, format=None):
        if self.request.user.is_worker:
            user = User.objects.get(id=id)
            serializer = self.serializer_class(user, request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                print("Not valid")
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            print("Not worker")
            return Response({"msg":"Not a worker"}, status=status.HTTP_400_BAD_REQUEST)


class WorkerDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if self.request.user.is_worker:
            worker = request.user
            applied_job = ApplyJob.objects.filter(worker=worker).count()
            confirmed_jobs = ApplyJob.objects.filter(worker=worker, confirmed=True).count()
            pending_jobs = ApplyJob.objects.filter(worker=worker, confirmed=False).count()

            data = {
                'applied_job':applied_job,
                'confirmed_jobs':confirmed_jobs,
                'pending_jobs':pending_jobs,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'msg':"Not a worker"}, status=status.HTTP_401_UNAUTHORIZED)


