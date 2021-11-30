from typing import Optional

import mysql.connector as sql
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.database.connection.database_connection_abc import \
    DatabaseConnectionABC
from cpl_core.database.database_settings import DatabaseSettings
from cpl_core.utils.credential_manager import CredentialManager
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.cursor import MySQLCursorBuffered


class DatabaseConnection(DatabaseConnectionABC):
    r"""Representation of the database connection
    """

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

    def connect(self, database_settings: DatabaseSettings):
        try:
            connection = sql.connect(
                host=database_settings.host,
                user=database_settings.user,
                passwd=CredentialManager.decrypt(database_settings.password),
                charset=database_settings.charset,
                use_unicode=database_settings.use_unicode,
                buffered=database_settings.buffered,
                auth_plugin=database_settings.auth_plugin
            )
            connection.cursor().execute(f'CREATE DATABASE IF NOT EXISTS `{database_settings.database}`;')
            self._database = sql.connect(
                host=database_settings.host,
                user=database_settings.user,
                passwd=CredentialManager.decrypt(database_settings.password),
                db=database_settings.database,
                charset=database_settings.charset,
                use_unicode=database_settings.use_unicode,
                buffered=database_settings.buffered,
                auth_plugin=database_settings.auth_plugin
            )
            self._cursor = self._database.cursor()
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line(f'[{__name__}] Connected to database')
            Console.set_foreground_color(ForegroundColorEnum.default)
        except Exception as e:
            Console.set_foreground_color(ForegroundColorEnum.red)
            Console.write_line(f'[{__name__}] Database connection failed -> {e}')
            Console.set_foreground_color(ForegroundColorEnum.default)
            exit()
