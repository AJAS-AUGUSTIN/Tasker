import imp
from unicodedata import name
from django.urls import path

from .views import WorkerDashboard
from .views import AppliedJobs, ApplyJobs, ApprovedJobs, SearchJobs, SearchUser, ViewAllJobs, JobItem, UpdateProfileView

urlpatterns = [
    path('apply_job/',ApplyJobs.as_view(),name='apply_job'),
    path('applied_jobs/',AppliedJobs.as_view(),name='applied_jobs'),
    path('approved_jobs/',ApprovedJobs.as_view(),name='approved_jobs'),
    path('view_all_jobs/',ViewAllJobs.as_view(),name='view_all_jobs'),
    path('jobitem/<int:id>/',JobItem.as_view()),
    path('search/jobs/',SearchJobs.as_view(),name='search'),
    path('search/user/',SearchUser.as_view(),name='search_user'),
    path('update_profile/<int:id>/', UpdateProfileView.as_view(), name='auth_update_profile'),
    path('dashboard/',WorkerDashboard.as_view(),name='worker_dashboard'),
    


]