from datetime import datetime

from sh_edraft.hosting.base.application_host_base import ApplicationHostBase
from sh_edraft.hosting.base.environment_base import EnvironmentBase
from sh_edraft.service.service_provider import ServiceProvider


class ApplicationHost(ApplicationHostBase):

    def __init__(self, name: str, env: EnvironmentBase):
        ApplicationHostBase.__init__(self)
        self._name: str = name
        self._environment: EnvironmentBase = env

        self._services = ServiceProvider(self)
        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()

    @property
    def name(self) -> str:
        return self._name
        
    @property
    def environment(self) -> EnvironmentBase:
        return self._environment

    @property
    def services(self):
        return self._services

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime):
        self._end_time = end_time

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: datetime):
        self._start_time = start_time

    @property
    def date_time_now(self) -> datetime:
        return datetime.now()
