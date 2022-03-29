from unicodedata import name
from django.urls import path
from user.models import ReviewRating
from user.views import AddJob, AppliedWorkersView, ApprovedWorkersView, ConfirmJob, Dashboard, JobItem, JobView, MarkAsCompleted, OverallRating, RemoveWorkerFromJob, SearchWorker, SingleWorkerView, UpdateProfileView, ViewReviewRating, WorkerReviewsView, WorkerView, SearchJobs, ReviewRatings

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('addjob/', AddJob.as_view(), name='addjob'),
    path('jobitem/<int:id>/', JobItem.as_view()),
    path('jobview/', JobView.as_view()),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),
         name='auth_update_profile'),
    path('confirm_job/<int:id>/', ConfirmJob.as_view(), name='confirm_job'),
    path('applied_workers/', AppliedWorkersView.as_view(), name='applied_worker'),
    path('approved_users/', ApprovedWorkersView.as_view(), name='approved_users'),
    path('worker_view/', WorkerView.as_view(), name='worker_view'),
    path('single_worker_view/<int:id>/',
         SingleWorkerView.as_view(), name='single_worker_view'),
    path('search/jobs/', SearchJobs.as_view(), name='search'),
    path('search/worker/',SearchWorker.as_view(),name='search_worker'),
    path('mark_as_completed/<int:id>/',MarkAsCompleted.as_view(),name='mark_as_completed'),
    path('remove_worker/<int:id>/',RemoveWorkerFromJob.as_view(),name='remove_worker'),
    path('review/<int:id>/',ReviewRatings.as_view(),name='review'),
    path('view_review/<int:id>/',ViewReviewRating.as_view(),name='view_review_rating'),
    path('worker_review_view/<int:id>/',WorkerReviewsView.as_view(),name='worker_review_view'),
    path('overall_rating/<int:id>/',OverallRating.as_view(),name='overall_rating'),


]
