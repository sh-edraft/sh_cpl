from typing import Optional

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from sh_edraft.database.connection.base.database_connection_base import DatabaseConnectionBase
from sh_edraft.database.model.database_settings import DatabaseSettings
from sh_edraft.console.console import Console
from sh_edraft.console.model.foreground_color import ForegroundColor


class DatabaseConnection(DatabaseConnectionBase):

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseConnectionBase.__init__(self)

        self._db_settings = database_settings

        self._engine: Optional[engine] = None
        self._session: Optional[Session] = None
        self._credentials: Optional[str] = None

    @property
    def engine(self) -> engine:
        return self._engine

    @property
    def session(self) -> Session:
        return self._session

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
            Console.set_foreground_color(ForegroundColor.green)
            Console.write_line(f'[{__name__}] Connected to database')
            Console.set_foreground_color(ForegroundColor.default)
        except Exception as e:
            Console.set_foreground_color(ForegroundColor.red)
            Console.write_line(f'[{__name__}] Database connection failed -> {e}')
            Console.set_foreground_color(ForegroundColor.default)
            exit()

