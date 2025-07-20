from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from reports.tasks import process_report_task

from .serializers import ReportUploadSerializer


class ReportUploadAPIView(APIView):
    def post(self, request: Request, *args, **kwargs):
        """Handles the POST request for file upload"""
        serializer = ReportUploadSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        report_type = validated_data['report_type']
        uploaded_file = validated_data['report_file']

        media_path = settings.MEDIA_ROOT / 'reports'
        fs = FileSystemStorage(location=media_path)
        file_name = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(file_name)

        task = process_report_task.delay(report_type=report_type, file_path=file_path)

        response_data = {
            'message': 'Report accepted for processing.',
            'report_type': report_type,
            'task_id': task.id
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
