from typing import Optional

import mysql.connector as sql
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursorBuffered

from cpl_core.database.connection.database_connection_abc import DatabaseConnectionABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.utils.credential_manager import CredentialManager


class DatabaseConnection(DatabaseConnectionABC):
    r"""Representation of the database connection"""

    def __init__(self):
        DatabaseConnectionABC.__init__(self)

        self._database: Optional[MySQLConnectionAbstract] = None
        self._cursor: Optional[MySQLCursorBuffered] = None

    @property
    def server(self) -> MySQLConnectionAbstract:
        return self._database

    @property
    def cursor(self) -> MySQLCursorBuffered:
        return self._cursor

    def connect(self, settings: DatabaseSettings):
        connection = sql.connect(
            host=settings.host,
            port=settings.port,
            user=settings.user,
            passwd=CredentialManager.decrypt(settings.password),
            charset=settings.charset,
            use_unicode=settings.use_unicode,
            buffered=settings.buffered,
            auth_plugin=settings.auth_plugin,
            ssl_disabled=settings.ssl_disabled,
        )
        connection.cursor().execute(f"CREATE DATABASE IF NOT EXISTS `{settings.database}`;")
        self._database = sql.connect(
            host=settings.host,
            port=settings.port,
            user=settings.user,
            passwd=CredentialManager.decrypt(settings.password),
            db=settings.database,
            charset=settings.charset,
            use_unicode=settings.use_unicode,
            buffered=settings.buffered,
            auth_plugin=settings.auth_plugin,
            ssl_disabled=settings.ssl_disabled,
        )
        self._cursor = self._database.cursor()
