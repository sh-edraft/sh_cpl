from abc import ABC, abstractmethod
from datetime import datetime


class ApplicationHostBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def start_time(self) -> datetime: pass

    @start_time.setter
    def start_time(self, start_time: datetime): pass

    @property
    @abstractmethod
    def end_time(self): pass

    @end_time.setter
    def end_time(self, end_time: datetime): pass
