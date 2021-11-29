from abc import ABC, abstractmethod

from cpl_core.database.database_settings import DatabaseSettings


class DatabaseContextABC(ABC):
    r"""ABC for the :class:`cpl_core.database.context.database_context.DatabaseContext`"""

    @abstractmethod
    def __init__(self, *args):
        pass

    @property
    @abstractmethod
    def cursor(self): pass

    @abstractmethod
    def connect(self, database_settings: DatabaseSettings):
        r"""Connects to a database by connection settings

        Parameter
        ---------
            database_settings :class:`cpl_core.database.database_settings.DatabaseSettings`
        """
        pass

    def save_changes(self):
        r"""Saves changes of the database"""
        pass
