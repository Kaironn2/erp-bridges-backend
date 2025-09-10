from typing import Literal

from celery import shared_task
import os
from reports.ingestion import REPORT_MAP
import logging

logger = logging.getLogger(__name__)

report_type = Literal['mgt_buy_orders_csv', 'mgt_customers_csv']


@shared_task
def process_report_task(report_type: report_type, file_path: str):
    """Celery task to process a report asynchronously"""
    try:
        PipelineClass = REPORT_MAP[report_type]
        pipeline = PipelineClass()
        pipeline.run(file_path)
        return f'Report {report_type} processed successfully from file {file_path}'
    except Exception as e:
        logger.exception('Report processing failed')
        raise ValueError(f'Report processment failed: {e}')
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
