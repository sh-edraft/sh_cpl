from abc import abstractmethod, ABC

from sqlalchemy import engine
from sqlalchemy.orm import Session


class DatabaseConnectionBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def engine(self) -> engine: pass

    @property
    @abstractmethod
    def session(self) -> Session: pass

    @abstractmethod
    def connect(self, connection_string: str): pass
