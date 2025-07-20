import io
from unittest.mock import MagicMock, patch

import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_report_upload_success(
    api_client,
    customers_valid_csv_byte_string,
    mock_file_storage
):
    """
    Tests the successful upload of a report file via the API endpoint,
    verifying the response and that the Celery task is dispatched correctly.
    """
    mock_file = io.BytesIO(customers_valid_csv_byte_string)
    mock_file.name = 'customers.csv'

    post_data = {
        'report_type': 'mgt_customers',
        'report_file': mock_file,
    }

    with patch('reports.tasks.process_report_task.delay') as mock_task_delay:
        mock_task_delay.return_value = MagicMock(id="mock-task-id-123")

        url = reverse('v1:api-upload-report', kwargs={'version': 'v1'})
        response = api_client.post(url, data=post_data, format='multipart')

        assert response.status_code == status.HTTP_202_ACCEPTED
        response_json = response.json()
        assert response_json['message'] == "Report accepted for processing."
        assert response_json['task_id'] == "mock-task-id-123"

        mock_task_delay.assert_called_once()
        call_args, call_kwargs = mock_task_delay.call_args
        assert call_kwargs['report_type'] == 'mgt_customers'
        assert 'file_path' in call_kwargs
        assert call_kwargs['file_path'].endswith('/tmp/fake_report_name.csv')
