
from typing import Optional

from cpl_core.console.console import Console
from cpl_core.database.connection.database_connection import DatabaseConnection
from cpl_core.database.connection.database_connection_abc import \
    DatabaseConnectionABC
from cpl_core.database.context.database_context_abc import DatabaseContextABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.database.table_abc import TableABC


class DatabaseContext(DatabaseContextABC):
    r"""Representation of the database context

    Parameter
    ---------
        database_settings: :class:`cpl_core.database.database_settings.DatabaseSettings`
    """

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseContextABC.__init__(self, database_settings)

        self._db: DatabaseConnectionABC = DatabaseConnection()
        self._cursor: Optional[str] = None
        self._tables: list[TableABC] = TableABC.__subclasses__()

    @property
    def cursor(self):
        return self._cursor

    def connect(self, database_settings: DatabaseSettings):
        self._db.connect(database_settings)
        c = self._db.server.cursor()
        self._cursor = c
        Console.write_line(f"Ts: {self._tables}")
        for table in self._tables:
            Console.write_line(f"{table}, {table.create_string}")
            c.execute(table.create_string)

    def save_changes(self):
        self._db.server.commit()
