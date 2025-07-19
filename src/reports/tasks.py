from celery import shared_task

from reports.services import process_report


@shared_task
def process_report_task(report_type: str, file_path: str):
    """Celery task to process a report asynchronously"""
    try:
        result = process_report(report_type=report_type, file_path_or_buffer=file_path)
        return result
    except Exception as e:
        raise ValueError(f'Report processment failed: {e}')
