import pathlib
from datetime import datetime

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC


class ApplicationRuntime(ApplicationRuntimeABC):

    def __init__(self, config: ConfigurationABC):
        ApplicationRuntimeABC.__init__(self)

        self._app_configuration = config
        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()
        self._working_directory = pathlib.Path().absolute()
        self._runtime_directory = pathlib.Path(__file__).parent.absolute()

    @property
    def configuration(self) -> ConfigurationABC:
        return self._app_configuration

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime):
        self._end_time = end_time

    @property
    def date_time_now(self) -> datetime:
        return datetime.now()

    @property
    def working_directory(self) -> str:
        return self._working_directory

    def set_working_directory(self, path: str = ''):
        if path != '':
            self._working_directory = path
            return

        self._working_directory = pathlib.Path().absolute()

    @property
    def runtime_directory(self) -> str:
        return self._runtime_directory

    def set_runtime_directory(self, file: str):
        self._runtime_directory = pathlib.Path(file).parent.absolute()
