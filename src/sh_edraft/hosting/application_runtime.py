from datetime import datetime

from sh_edraft.configuration.base.configuration_base import ConfigurationBase
from sh_edraft.hosting.base.environment_base import EnvironmentBase
from sh_edraft.hosting.base.application_runtime_base import ApplicationRuntimeBase


class ApplicationRuntime(ApplicationRuntimeBase):

    def __init__(self, config: ConfigurationBase, runtime: EnvironmentBase):
        ApplicationRuntimeBase.__init__(self)

        self._app_runtime = runtime
        self._app_configuration = config
        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()

    @property
    def environment(self) -> EnvironmentBase:
        return self._app_runtime
    
    @property
    def configuration(self) -> ConfigurationBase:
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
