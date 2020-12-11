from abc import abstractmethod, ABC

from sqlalchemy import engine
from sqlalchemy.orm import session


class DatabaseConnectionBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def engine(self) -> engine: pass

    @property
    @abstractmethod
    def session(self) -> session: pass

    @abstractmethod
    def connect(self, connection_string: str): pass
