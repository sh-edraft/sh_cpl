import os
from datetime import datetime
from socket import gethostname
from typing import Optional

from cpl.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl.environment.environment_name_enum import EnvironmentNameEnum


class ApplicationEnvironment(ApplicationEnvironmentABC):

    def __init__(self, name: EnvironmentNameEnum = EnvironmentNameEnum.production):
        """
        Represents environment of the application
        :param name:
        """
        ApplicationEnvironmentABC.__init__(self)

        self._environment_name: Optional[EnvironmentNameEnum] = name
        self._app_name: Optional[str] = None
        self._customer: Optional[str] = None

        self._start_time: datetime = datetime.now()
        self._end_time: datetime = datetime.now()
        self._working_directory = os.path.abspath('./')
        self._runtime_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @property
    def environment_name(self) -> str:
        return str(self._environment_name.value)

    @environment_name.setter
    def environment_name(self, environment_name: str):
        self._environment_name = EnvironmentNameEnum(environment_name)

    @property
    def application_name(self) -> str:
        return self._app_name if self._app_name is not None else ''

    @application_name.setter
    def application_name(self, application_name: str):
        self._app_name = application_name

    @property
    def customer(self) -> str:
        return self._customer if self._customer is not None else ''

    @customer.setter
    def customer(self, customer: str):
        self._customer = customer

    @property
    def host_name(self):
        return gethostname()

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
        return str(self._working_directory)

    @property
    def runtime_directory(self) -> str:
        return str(self._runtime_directory)

    def set_runtime_directory(self, runtime_directory: str):
        if runtime_directory != '':
            self._runtime_directory = runtime_directory
            return

        self._runtime_directory = pathlib.Path().absolute()

    def set_working_directory(self, working_directory: str):
        if working_directory != '':
            self._working_directory = working_directory
            return

        self._working_directory = pathlib.Path().absolute()
