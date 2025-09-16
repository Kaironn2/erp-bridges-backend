from typing import Dict

from buy_order.models import Status


class StatusRepository:
    def find_all_as_dict(self) -> Dict[str, Status]:
        return {s.name: s for s in Status.objects.all()}

    def filter_by_names(self, names: list[str]) -> list[Status]:
        return list(Status.objects.filter(name__in=names))

    def get_or_create(self, name: str) -> Status:
        status, created = Status.objects.get_or_create(name=name)
        return status
