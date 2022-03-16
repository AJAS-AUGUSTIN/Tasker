from django.urls import path, include
from .views import LogOut, UserRegistration, WorkerRegistration
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('user/register/', UserRegistration.as_view(), name='userregister'),
    path('worker/register/', WorkerRegistration.as_view(), name='workerregister'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogOut.as_view(), name='logout'),
    # path('accounts/', include('allauth.urls')),

]
