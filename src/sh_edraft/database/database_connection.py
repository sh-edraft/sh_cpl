from typing import Optional

from sqlalchemy import engine, create_engine
from sqlalchemy.orm import session, sessionmaker

from sh_edraft.database.base.database_connection_base import DatabaseConnectionBase
from sh_edraft.database.model.database_settings import DatabaseSettings


class DatabaseConnection(DatabaseConnectionBase):

    def __init__(self, database_settings: DatabaseSettings):
        DatabaseConnectionBase.__init__(self)

        self._db_settings = database_settings

        self._engine: Optional[engine] = None
        self._session: Optional[session] = None
        self._credentials: Optional[str] = None

    def create(self):
        self._engine = create_engine(self._db_settings.decrypted_connection_string)

        if self._db_settings.encoding is not None:
            self._engine.encoding = self._db_settings.encoding

        if self._db_settings.case_sensitive is not None:
            self._engine.case_sensitive = self._db_settings.case_sensitive

        if self._db_settings.echo is not None:
            self._engine.echo = self._db_settings.echo

        db_session = sessionmaker(bind=self._engine)
        self._session = db_session()

