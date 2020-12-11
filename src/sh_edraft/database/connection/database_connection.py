from typing import Optional

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import session, sessionmaker

from sh_edraft.database.connection.base.database_connection_base import DatabaseConnectionBase
from sh_edraft.database.model.database_settings import DatabaseSettings
from sh_edraft.utils.console import Console


class DatabaseConnection(DatabaseConnectionBase):

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseConnectionBase.__init__(self)

        self._db_settings = database_settings

        self._engine: Optional[engine] = None
        self._session: Optional[session] = None
        self._credentials: Optional[str] = None

        self.create()

    @property
    def engine(self) -> engine:
        return self._engine

    @property
    def session(self) -> session:
        return self._session

    def create(self): pass

    def connect(self, connection_string: str):
        try:
            self._engine = create_engine(connection_string)

            if self._db_settings.encoding is not None:
                self._engine.encoding = self._db_settings.encoding

            if self._db_settings.case_sensitive is not None:
                self._engine.case_sensitive = self._db_settings.case_sensitive

            if self._db_settings.echo is not None:
                self._engine.echo = self._db_settings.echo

            self._engine.connect()

            db_session = sessionmaker(bind=self._engine)
            self._session = db_session()
            Console.write_line(f'[{__name__}] Connected to database', 'green')
        except Exception as e:
            Console.write_line(f'[{__name__}] Database connection failed -> {e}', 'red')
            exit()

