import os
import tempfile
import logging
from typing import cast

from celery import Task
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from reports.api.v1.serializers import (
    ReportUploadSerializer,
)
from reports.tasks import process_report_task

logger = logging.getLogger(__name__)


class ReportUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ReportUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = cast(dict, serializer.validated_data)

        report_type = validated_data['report_type']
        uploaded_file = validated_data['report_file']

        suffix = os.path.splitext(getattr(uploaded_file, 'name', ''))[1]
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            task = cast(Task, process_report_task)
            task.delay(report_type, tmp_path)

            return Response(
                {'detail': 'Report processing started.', 'report_type': report_type},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as exc:
            logger.exception('Failed to start report ingestion for report_type=%s', report_type)
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
            return Response(
                {'detail': 'Failed to start report ingestion.', 'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
