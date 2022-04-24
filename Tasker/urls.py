from django.urls import path, include
from accounts import urls
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


urlpatterns = [

    path('accounts/', include('accounts.urls')),
    path('admin/', include('admin.urls')),
    path('user/', include('user.urls')),
    path('worker/', include('worker.urls')),
    path('chat/', include('chat.urls')),
    path('openapi-schema', get_schema_view(
        title="Tasker",
        description="The destination of job givers and seekers...",
        version="1.0.0",
        public=True
    ), name='openapi-schema'),

    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

]
