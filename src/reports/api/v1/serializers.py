from rest_framework import serializers

from reports.ingestion.mapping import REPORT_MAP


class ReportUploadSerializer(serializers.Serializer):
    """
    Handles a validation for the report upload endpoint
    Ensures a valid report_type is selected and a file is provided
    """

    report_type = serializers.ChoiceField(choices=list(REPORT_MAP.keys()))
    report_file = serializers.FileField()
