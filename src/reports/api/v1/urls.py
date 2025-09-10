from django.urls import path

from .views import ReportUploadView

app_name = 'v1'

urlpatterns = [path('upload/', ReportUploadView.as_view(), name='api-upload-report')]
