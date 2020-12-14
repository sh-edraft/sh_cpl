from sqlalchemy import engine, Table
from sqlalchemy.orm import Session

from sh_edraft.database.connection.database_connection import DatabaseConnection
from sh_edraft.database.connection.base.database_connection_base import DatabaseConnectionBase
from sh_edraft.database.context.base.database_context_base import DatabaseContextBase
from sh_edraft.database.model.dbmodel import DBModel
from sh_edraft.database.model.database_settings import DatabaseSettings
from sh_edraft.utils.console import Console


class DatabaseContext(DatabaseContextBase):

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseContextBase.__init__(self)

        self._db: DatabaseConnectionBase = DatabaseConnection(database_settings)
        self._tables: list[Table] = []

    @property
    def engine(self) -> engine:
        return self._db.engine

    @property
    def session(self) -> Session:
        return self._db.session

    def create(self):
        pass

    def connect(self, connection_string: str):
        self._db.connect(connection_string)
        self._create_tables()

    def _create_tables(self):
        try:
            for subclass in DBModel.__subclasses__():
                self._tables.append(subclass.__table__)

            DBModel.metadata.drop_all(self._db.engine, self._tables)
            DBModel.metadata.create_all(self._db.engine, self._tables, checkfirst=True)
            Console.write_line(f'[{__name__}] Created tables', 'green')
        except Exception as e:
            Console.write_line(f'[{__name__}] Creating tables failed -> {e}', 'red')
            exit()
