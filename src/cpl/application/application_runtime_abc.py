from abc import ABC, abstractmethod
from datetime import datetime

from cpl.configuration.configuration_abc import ConfigurationABC


class ApplicationRuntimeABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def configuration(self) -> ConfigurationABC: pass

    @property
    @abstractmethod
    def start_time(self) -> datetime: pass

    @start_time.setter
    @abstractmethod
    def start_time(self, start_time: datetime): pass

    @property
    @abstractmethod
    def end_time(self): pass

    @end_time.setter
    @abstractmethod
    def end_time(self, end_time: datetime): pass

    @property
    @abstractmethod
    def date_time_now(self) -> datetime: pass

    @property
    @abstractmethod
    def working_directory(self) -> str: pass

    @property
    @abstractmethod
    def runtime_directory(self) -> str: pass

    @abstractmethod
    def set_runtime_directory(self, runtime_directory: str): pass
