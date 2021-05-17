from abc import abstractmethod, ABC

from sqlalchemy import engine
from sqlalchemy.orm import Session


class DatabaseConnectionABC(ABC):
    r"""ABC for the :class:`cpl.database.connection.database_connection.DatabaseConnection`"""

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def engine(self) -> engine: pass

    @property
    @abstractmethod
    def session(self) -> Session: pass

    @abstractmethod
    def connect(self, connection_string: str):
        r"""Connects to a database by connection string

        Parameter
        ---------
            connection_string: :class:`str`
                Database connection string, see: https://docs.sqlalchemy.org/en/14/core/engines.html
        """
        pass
