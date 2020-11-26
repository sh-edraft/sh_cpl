from abc import ABC, abstractmethod
from datetime import datetime

from sh_edraft.hosting.base.environment_base import EnvironmentBase


class ApplicationHostBase(ABC):

    @abstractmethod
    def __init__(self): pass
    
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def environment(self) -> EnvironmentBase: pass

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
