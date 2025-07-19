import io
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

pytestmark = pytest.mark.django_db


def test_report_upload_success(api_client, customers_valid_csv_byte_string):
    mock_file = io.BytesIO(customers_valid_csv_byte_string)
    mock_file.name = 'customers.csv'

    post_data = {
        'report_type': 'mgt_customers',
        'report_file': mock_file,
    }

    with patch('reports.tasks.process_report_task') as mock_task_delay:
        url = reverse('v1:api-upload-report', kwargs={'version': 'v1'})
        response: Response = api_client.post(url, data=post_data, format='multipart')

        assert response.status_code == status.HTTP_202_ACCEPTED
        response_json = response.json()
        assert response_json['message'] == 'Report accepted for processing.'
        assert response_json['report_type'] == 'mgt_customers'
        assert 'task_id' in response_json

        mock_task_delay.assert_called_once()

        call_args, call_kwargs = mock_task_delay.call_args
        assert call_kwargs['report_type'] == 'mgt_customers'
        assert 'file_path' in call_kwargs
        assert call_kwargs['file_path'].endswith('customers.csv')
