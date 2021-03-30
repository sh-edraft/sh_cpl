from abc import abstractmethod, ABC

from sqlalchemy import engine
from sqlalchemy.orm import Session


class DatabaseContextABC(ABC):

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
        """
        Connects to a database with connection string
        :param connection_string:
        :return:
        """
        pass

    def save_changes(self):
        """
        Saves changes of the database
        """
        pass

    @abstractmethod
    def _create_tables(self):
        """
        Create all tables for application from database model
        :return:
        """
        pass
