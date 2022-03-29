from ast import Delete
from distutils.log import error
from urllib import request
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts import permissionss, serializers
from accounts.models import User
from accounts.permissionss import IsOwner
from worker.models import ApplyJob
from .serializers import ConfirmJobSerializer, JobSerializer, MarkAsCompletedSerializer, RemoveWorkerSerializer, UpdateUserSerializer, AppliedWorkersViewSerializer, ViewReviewRatingSerializer, WorkerViewSerializer, ReviewRatingSerializer
from .models import Job, ReviewRating
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class Dashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        total_jobs_posted = Job.objects.filter(user=user).count()
        jobs = Job.objects.filter(user=user)
        applied_workers_for_job = ApplyJob.objects.filter(job__in=jobs).count()
        completed_works = Job.objects.filter(user=user, completed=True).count()
        pending_works = Job.objects.filter(user=user, completed=False).count()
        print(completed_works, "completed_works")
        data = {
            'total_jobs_posted': total_jobs_posted,
            'applied_workers_for_job': applied_workers_for_job,
            'completed_works': completed_works,
            'pending_works': pending_works
        }
        return Response(data, status=status.HTTP_200_OK)


class AddJob(APIView):
    # authentication_classes = [BasicAuthentication]

    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class JobView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer

    def get(self, request, format=None):
        data = Job.objects.filter(user=request.user)
        serializer = self.serializer_class(data, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_201_CREATED)


class JobItem(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = JobSerializer

    def get_object(self, id):
        try:
            data = Job.objects.get(id=id)
            self.check_object_permissions(self.request, data)
            return data
        except:
            raise Http404

    def get(self, request, id, format=None):
        serializer = self.serializer_class(self.get_object(id))
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        data = self.get_object(id)
        serializer = self.serializer_class(
            data, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        data = self.get_object(id)
        data.delete()
        return Response(status=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class ConfirmJob(APIView):
    serializer_class = ConfirmJobSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get(self, request, id, format=None):
        try:
            data = ApplyJob.objects.get(id=id)
            if data.job.user == self.request.user:
                serializer = self.serializer_class(data)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        data = ApplyJob.objects.get(id=id)
        job = Job.objects.filter(id=data.job.id)
        if data.job.user == self.request.user:
            if data.confirmed == True:
                return Response({"msg": "Already Confirmed"})
            else:
                data.confirmed = True
                data.save()
                for i in job:
                    i.worker = data.worker
                    i.save()
                serializer = self.serializer_class(data)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # def put(self, request, id, format=None):
    #     data = ApplyJob.objects.get(id=id)
    #     if data.job.user == self.request.user:
    #         serializer = self.serializer_class(
    #             data, data=request.data, context={'request': request})
    #         if serializer.is_valid():
    #             serializer.save()
    #             serialized_data = serializer.data
    #             return Response(serialized_data, status=status.HTTP_200_OK)
    #         else:
    #             return Response(status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)


class AppliedWorkersView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get(self, request, format=None):
        if self.request.user.is_user:
            jobs = Job.objects.filter(user=request.user)
            data = ApplyJob.objects.filter(job__in=jobs)
            serializer = AppliedWorkersViewSerializer(data, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Not a user"}, status=status.HTTP_401_UNAUTHORIZED)


class ApprovedWorkersView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, format=None):
        if self.request.user.is_user:
            jobs = Job.objects.filter(user=request.user)
            data = ApplyJob.objects.filter(job__in=jobs, confirmed=True)
            serializer = AppliedWorkersViewSerializer(data, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        else:
            return Response({"msg": "Not a user"}, status=status.HTTP_401_UNAUTHORIZED)


class WorkerView(APIView):

    def get(self, request, format=None):
        data = User.objects.filter(is_worker=True)
        serializer = WorkerViewSerializer(data, many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class SingleWorkerView(APIView):
    def get(self, request, id, format=None):
        try:
            data = User.objects.get(id=id, is_worker=True)
        except:
            return Response({"msg": "Worker does not exist"})
        serializer = WorkerViewSerializer(data)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class SearchJobs(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'category__title',
                     'minimum_wage', 'city', 'landmark', 'requirements']
    filterset_fields = ['title', 'category', 'minimum_wage', 'city', 'user']


class SearchWorker(generics.ListAPIView):
    queryset = User.objects.filter(is_worker=True)
    serializer_class = WorkerViewSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['username', 'first_name', 'last_name',
                     'email', 'phone_number']
    filterset_fields = ['username']


class MarkAsCompleted(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [BasicAuthentication]

    serializer_class = MarkAsCompletedSerializer

    def put(self, request, id, format=None):
        try:
            job = Job.objects.get(id=id)
            if job.user == self.request.user:
                if job.completed == True:
                    return Response({"msg": "Alredy Completed"})
                else:
                    job.completed = True
                    job.save()
                    serializer = self.serializer_class(job)
                    serialized_data = serializer.data
                    return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "No permission"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class RemoveWorkerFromJob(APIView):
    serializer_class = RemoveWorkerSerializer

    def put(self, request, id, format=None):
        data = Job.objects.get(id=id)
        data.worker = None
        data.save()
        serializer = self.serializer_class(data)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class ReviewRatings(APIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [BasicAuthentication]

    def post(self, request, id, format=None):
        try:
            job = Job.objects.get(id=id)
            if job.user == request.user:
                print("User Trrrrrrrrue")
                if job.review == False:
                    print("yesssssssssss")
                    worker = job.worker
                    job.review = True
                    job.save()
                    print(worker)
                    user = job.user
                    print(user)
                    data = request.data
                    serializer = self.serializer_class(data=data)
                    print(serializer)
                    if serializer.is_valid():
                        print("1111111111111111111")
                        serializer.save(job=job, user=user, worker=worker)
                        serialized_data = serializer.data
                        return Response(serialized_data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    print("truuuuuuuu")
                    return Response({'msg': 'Already Reviewed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("44444444444444")
                return Response({'msg': 'No Permission'})
        except:
            return Response({'msg': "Error"})


class ViewReviewRating(APIView):
    serializer_class = ViewReviewRatingSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes = [BasicAuthentication]

    def get(self, request, id, format=None):
        try:
            job = Job.objects.get(id=id)
            if job.user == request.user:
                print("Job", job)
                data = ReviewRating.objects.get(job=job)
                print("data", data)
                serializer = self.serializer_class(data)
                serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Permission'})
        except:
            return Response({"msg": "No rating and Review"})

    def put(self, request, id, format=None):
        try:
            job = Job.objects.get(id=id)
            if job.user == request.user:
                data = ReviewRating.objects.get(job=job)
                serializer = self.serializer_class(data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    serialized_data = serializer.data
                return Response(serialized_data, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Permission'})
        except:
            return Response({"msg": "Error in editing"})

    def delete(self, request, id, format=None):
        try:
            job = Job.objects.get(id=id)
            if job.user == request.user:
                data = ReviewRating.objects.get(job=job)
                data.delete()
                return Response({'msg': "Deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'No Permission'})
        except:
            return Response({"msg": "Error in finding out review"})


class WorkerReviewsView(APIView):
    def get(self, request, id, format=None):
        try:
            data = ReviewRating.objects.filter(worker=id)
            print(data)
            serializer = ViewReviewRatingSerializer(data, many=True)
            serialized_data = serializer.data
            return Response(serialized_data, status=status.HTTP_200_OK)
        except:
            return Response({'msg': "No Reviews"})


class OverallRating(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id, format=None):
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        try:
            data = ReviewRating.objects.filter(worker=id)
            for i in data:
                print(i.rating)
                if i.rating == 5:
                    print("Kerii")
                    count5 += 1
                    print(count5)
                elif i.rating == 4:
                    count4 += 1
                elif i.rating == 3:
                    count3 += 1
                elif i.rating == 2:
                    count2 += 1
                elif i.rating == 1:
                    count1 += 1
                average = ((5*count5)+(4*count4)+(3*count3)+(2*count2) +
                           (1*count1))/(count5+count4+count3+count2+count1)
                print("Average", average)
                return Response({'average_rating': average}, status=status.HTTP_200_OK)
        except:
            return Response({'Rating': "No Rating"})
