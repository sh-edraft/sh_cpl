from sqlalchemy import engine, Table
from sqlalchemy.orm import Session

from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.database.connection.database_connection import DatabaseConnection
from cpl.database.connection.database_connection_abc import DatabaseConnectionABC
from cpl.database.context.database_context_abc import DatabaseContextABC
from cpl.database.database_settings import DatabaseSettings
from cpl.database.database_model import DatabaseModel


class DatabaseContext(DatabaseContextABC):
    r"""Representation of the database context

    Parameter
    ---------
        database_settings: :class:`cpl.database.database_settings.DatabaseSettings`
    """

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseContextABC.__init__(self)

        self._db: DatabaseConnectionABC = DatabaseConnection(database_settings)
        self._tables: list[Table] = []

    @property
    def engine(self) -> engine:
        return self._db.engine

    @property
    def session(self) -> Session:
        return self._db.session

    def connect(self, connection_string: str):
        self._db.connect(connection_string)
        self._create_tables()

    def save_changes(self):
        self._db.session.commit()

    def _create_tables(self):
        try:
            for subclass in DatabaseModel.__subclasses__():
                self._tables.append(subclass.__table__)

            DatabaseModel.metadata.drop_all(self._db.engine, self._tables)
            DatabaseModel.metadata.create_all(self._db.engine, self._tables, checkfirst=True)
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(f'[{__name__}] Created tables')
            Console.set_foreground_color(ForegroundColorEnum.default)
        except Exception as e:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(f'[{__name__}] Creating tables failed -> {e}')
            Console.set_foreground_color(ForegroundColorEnum.default)
            exit()