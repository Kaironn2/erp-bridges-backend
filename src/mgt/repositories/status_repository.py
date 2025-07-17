from mgt.models import Status


class StatusRepository:

    def get_or_create(self, name: str) -> Status:
        status, created = Status.objects.get_or_create(name=name)
        return status
