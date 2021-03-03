from abc import abstractmethod, ABC

from sqlalchemy import engine
from sqlalchemy.orm import Session


class DatabaseContextABC(ABC):

    @property
    @abstractmethod
    def engine(self) -> engine: pass

    @property
    @abstractmethod
    def session(self) -> Session: pass

    @abstractmethod
    def connect(self, connection_string: str): pass

    @abstractmethod
    def _create_tables(self): pass
