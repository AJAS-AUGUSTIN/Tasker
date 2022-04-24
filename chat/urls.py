
from django.urls import path
from .views import index, chatPage

urlpatterns = [
    path('', index.as_view(), name='home'),
    path('<str:username>', chatPage.as_view(), name='chat'),
]