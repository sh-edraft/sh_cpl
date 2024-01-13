from typing import Optional

import mysql

from cpl_core.database.connection.database_connection import DatabaseConnection
from cpl_core.database.connection.database_connection_abc import DatabaseConnectionABC
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.database.table_abc import TableABC
from mysql.connector.cursor import MySQLCursorBuffered


class DatabaseContext(DatabaseContextABC):
    r"""Representation of the database context

    Parameter:
        database_settings: :class:`cpl_core.database.database_settings.DatabaseSettings`
    """

    def __init__(self):
        DatabaseContextABC.__init__(self)

        self._db: DatabaseConnectionABC = DatabaseConnection()
        self._settings: Optional[DatabaseSettings] = None

    @property
    def cursor(self) -> MySQLCursorBuffered:
        self._ping_and_reconnect()
        return self._db.cursor

    def _ping_and_reconnect(self):
        try:
            self._db.server.ping(reconnect=True, attempts=3, delay=5)
        except Exception as err:
            # reconnect your cursor as you did in __init__ or wherever
            if self._settings is None:
                raise Exception("Call DatabaseContext.connect first")
            self.connect(self._settings)

    def connect(self, database_settings: DatabaseSettings):
        if self._settings is None:
            self._settings = database_settings
        self._db.connect(database_settings)

        self.save_changes()

    def save_changes(self):
        self._ping_and_reconnect()
        self._db.server.commit()

    def select(self, statement: str) -> list[tuple]:
        self._ping_and_reconnect()
        self._db.cursor.execute(statement)
        return self._db.cursor.fetchall()
