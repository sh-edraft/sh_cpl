from datetime import datetime

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC


class ApplicationRuntime(ApplicationRuntimeABC):

    def __init__(self, config: ConfigurationABC):
        ApplicationRuntimeABC.__init__(self)

        self._app_configuration = config
        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()

    @property
    def configuration(self) -> ConfigurationABC:
        return self._app_configuration

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, start_time: datetime):
        self._start_time = start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime):
        self._end_time = end_time

    @property
    def date_time_now(self) -> datetime:
        return datetime.now()
