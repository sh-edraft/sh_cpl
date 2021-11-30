from abc import ABC, abstractmethod

from cpl_core.database.database_settings import DatabaseSettings
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursorBuffered


class DatabaseConnectionABC(ABC):
    r"""ABC for the :class:`cpl_core.database.connection.database_connection.DatabaseConnection`"""

    @abstractmethod
    def __init__(self): pass

    @property
    @abstractmethod
    def server(self) -> MySQLConnectionAbstract: pass
    
    @property
    @abstractmethod
    def cursor(self) -> MySQLCursorBuffered: pass
    
    @abstractmethod
    def connect(self, database_settings: DatabaseSettings):
        r"""Connects to a database by connection string

        Parameter
        ---------
            connection_string: :class:`str`
                Database connection string, see: https://docs.sqlalchemy.org/en/14/core/engines.html
        """
        pass
