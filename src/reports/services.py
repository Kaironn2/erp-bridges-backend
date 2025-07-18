from typing import Any, Dict

from reports.strategies.base_strategy import BaseReportStrategy
from reports.strategies.mgt.buy_orders_report_strategy import MgtBuyOrdersReportStrategy
from reports.strategies.mgt.customers_report_strategy import MgtCustomersReportStrategy

STRATEGY_MAP = {
    'mgt_buy_orders': MgtBuyOrdersReportStrategy,
    'mgt_customers': MgtCustomersReportStrategy,
}


def process_report(report_type: str, file_path_or_buffer: Any) -> Dict[str, Any]:
    """
    The main entry point for processing any report.

    This function acts as a factory, selecting and executing the appropriate
    strategy based on the report_type.

    Args:
        report_type (str): The identifier for the report to be processed
                           (e.g., 'mgt_buy_orders').
        file_path_or_buffer: The file path or in-memory buffer for the report.

    Returns:
        Dict[str, Any]: A dictionary containing the results of the processing.

    Raises:
        ValueError: If the report_type is unknown.
    """
    strategy_class: BaseReportStrategy = STRATEGY_MAP.get(report_type)

    if not strategy_class:
        raise ValueError(f'Unknow report type: {report_type}')

    strategy: BaseReportStrategy = strategy_class(file_path_or_buffer)
    return strategy.process()
