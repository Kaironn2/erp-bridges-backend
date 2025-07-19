from django.urls import path

from .views import ReportUploadAPIView

app_name = 'v1'

urlpatterns = [
    path('upload/', ReportUploadAPIView.as_view(), name='api-upload-report')
]
