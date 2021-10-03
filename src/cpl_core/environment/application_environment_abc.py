from abc import ABC, abstractmethod
from datetime import datetime


class ApplicationEnvironmentABC(ABC):
    r"""ABC of the class :class:`cpl_core.environment.application_environment.ApplicationEnvironment`"""

    @abstractmethod
    def __init__(self):
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
        r"""Sets the current runtime directory

        Parameter
        ---------
            runtime_directory: :class:`str`
                Path of the runtime directory
        """
        pass

    @abstractmethod
    def set_working_directory(self, working_directory: str):
        r"""Sets the current working directory

        Parameter
        ---------
            working_directory: :class:`str`
                Path of the current working directory
        """
        pass
