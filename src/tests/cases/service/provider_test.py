import unittest

from sh_edraft.console import Console
from sh_edraft.database.context import DatabaseContext
from sh_edraft.hosting import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase


class ProviderTest(unittest.TestCase):

    def setUp(self):
        Console.disable()
        self._app_host = ApplicationHost()
        self._configuration = self._app_host.configuration
        self._services = self._app_host.services

        self._configuration.add_argument_variables()
        self._configuration.add_json_file(f'appsettings.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.environment_name}.json')
        self._configuration.add_json_file(f'appsettings.{self._configuration.environment.host_name}.json', optional=True)

    def test_get_db_context(self):
        self._services.add_db_context(DatabaseContext)
        db: DatabaseContext = self._services.get_db_context()

        self.assertIsNotNone(db)

    def test_get_service_singleton(self):
        self._services.add_singleton(LoggerBase, Logger)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNotNone(logger)

    def test_get_service_scoped(self):
        self._services.add_scoped(LoggerBase, Logger)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNotNone(logger)

    def test_get_service_transient(self):
        self._services.add_transient(LoggerBase, Logger)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNotNone(logger)

    def test_remove_service_singleton(self):
        self._services.add_singleton(LoggerBase, Logger)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNotNone(logger)

        self._services.remove_service(LoggerBase)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNone(logger)

    def test_remove_service_scoped(self):
        self._services.add_scoped(LoggerBase, Logger)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNotNone(logger)

        self._services.remove_service(LoggerBase)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNone(logger)

    def test_remove_service_transient(self):
        self._services.add_transient(LoggerBase, Logger)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNotNone(logger)

        self._services.remove_service(LoggerBase)
        logger = self._services.get_service(LoggerBase)

        self.assertIsNone(logger)
