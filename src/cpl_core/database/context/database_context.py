
from typing import Optional

from cpl_core.database.connection.database_connection import DatabaseConnection
from cpl_core.database.connection.database_connection_abc import \
    DatabaseConnectionABC
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.database.table_abc import TableABC
from mysql.connector.cursor import MySQLCursorBuffered


class DatabaseContext(DatabaseContextABC):
    r"""Representation of the database context

    Parameter
    ---------
        database_settings: :class:`cpl_core.database.database_settings.DatabaseSettings`
    """

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseContextABC.__init__(self, database_settings)

        self._db: DatabaseConnectionABC = DatabaseConnection()
        self._tables: list[TableABC] = TableABC.__subclasses__()

    @property
    def cursor(self) -> MySQLCursorBuffered:
        return self._db.cursor
    
    def connect(self, database_settings: DatabaseSettings):
        self._db.connect(database_settings)
        for table in self._tables:
            self._db.cursor.execute(table.get_create_string())

    def save_changes(self):
        self._db.server.commit()
        
    def select(self, statement: str) -> list[tuple]:
        self._db.cursor.execute(statement)
        return self._db.cursor.fetchall()
