from abc import abstractmethod, ABC

from sqlalchemy import engine
from sqlalchemy.orm import Session


class DatabaseContextABC(ABC):
    r"""ABC for the :class:`cpl_core.database.context.database_context.DatabaseContext`"""

    @abstractmethod
    def __init__(self, *args):
        pass

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

    def save_changes(self):
        r"""Saves changes of the database"""
        pass

    @abstractmethod
    def _create_tables(self):
        r"""Create all tables for application from database model"""
        pass
