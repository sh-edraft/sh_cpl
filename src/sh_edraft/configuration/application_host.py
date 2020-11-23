from datetime import datetime

from sh_edraft.service import ServiceProvider


class ApplicationHost:
    
    def __init__(self):
        self._services = ServiceProvider()
        self._end_time: datetime = datetime.now()
        self._start_time: datetime = datetime.now()

    @property
    def services(self):
        return self._services

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime) -> None:
        self._end_time = end_time

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: datetime) -> None:
        self._start_time = start_time

    @property
    def date_time_now(self) -> datetime:
        return datetime.now()
