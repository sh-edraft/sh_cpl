from abc import ABC, abstractmethod
from datetime import datetime


class ApplicationEnvironmentABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC of application environment
        """
        pass

    @property
    @abstractmethod
    def environment_name(self) -> str: pass

    @environment_name.setter
    @abstractmethod
    def environment_name(self, environment_name: str): pass

    @property
    @abstractmethod
    def application_name(self) -> str: pass

    @application_name.setter
    @abstractmethod
    def application_name(self, application_name: str): pass

    @property
    @abstractmethod
    def customer(self) -> str: pass

    @customer.setter
    @abstractmethod
    def customer(self, customer: str): pass

    @property
    @abstractmethod
    def content_root_path(self) -> str: pass

    @content_root_path.setter
    @abstractmethod
    def content_root_path(self, content_root_path: str): pass

    @property
    @abstractmethod
    def host_name(self) -> str: pass

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
    def set_runtime_directory(self, runtime_directory: str):
        """
        Sets the current runtime directory
        :param runtime_directory:
        :return:
        """
        pass
