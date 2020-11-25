from abc import ABC, abstractmethod
from datetime import datetime


class ApplicationHostBase(ABC):

    @abstractmethod
    def __init__(self): pass
