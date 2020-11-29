import unittest
from typing import cast

from sh_edraft.hosting import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.publishing import Publisher
from sh_edraft.publishing.base import PublisherBase
from sh_edraft.service import ServiceProvider
from sh_edraft.service.base import ServiceBase


class ServiceProviderTest(unittest.TestCase):

    def setUp(self):
        self._app_host = ApplicationHost()
        self._config = self._app_host.configuration
        self._config.create()
        self._config.add_environment_variables('PYTHON_')
        self._config.add_environment_variables('CPL_')
        self._config.add_argument_variables()
        self._config.add_json_file(f'appsettings.json')
        self._config.add_json_file(f'appsettings.{self._config.environment.environment_name}.json')
        self._config.add_json_file(f'appsettings.{self._config.environment.host_name}.json', optional=True)
        self._services: ServiceProvider = cast(ServiceProvider, self._app_host.services)
        self._services.create()

    def _check_general_requirements(self):
        self.assertIsNotNone(self._services)

    def _add_logger(self):
        self._services.add_singleton(LoggerBase, Logger)
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()

    def test_create(self):
        print(f'{__name__}.test_create:')
        provider = ServiceProvider(self._app_host.application_runtime)
        self.assertIsNotNone(provider)
        provider.create()
        self.assertIsNotNone(provider)

    def test_add_singleton(self):
        print(f'{__name__}.test_add_singleton:')
        self._check_general_requirements()

        self._services.add_singleton(LoggerBase, Logger)
        self.assertGreater(len(self._services._singleton_services), 0)

        found = False
        for service_type in self._services._singleton_services:
            service = self._services._singleton_services[service_type]
            if service_type == LoggerBase and (
                    isinstance(service, Logger) and
                    isinstance(service, LoggerBase) and
                    isinstance(service, ServiceBase)
            ):
                if not found:
                    found = True

        self.assertTrue(found)

        found = False
        for service_type in self._services._singleton_services:
            service = self._services._singleton_services[service_type]
            if service_type == PublisherBase and (
                    isinstance(service, Publisher) and
                    isinstance(service, PublisherBase) and
                    isinstance(service, ServiceBase)
            ):
                if not found:
                    found = True

        self.assertFalse(found)

    def test_get_singleton(self):
        print(f'{__name__}.test_get_singleton:')
        self._check_general_requirements()

        self._services.add_singleton(LoggerBase, Logger)
        logger: Logger = self._services.get_service(LoggerBase)
        self.assertIsNotNone(logger)
        self.assertTrue(isinstance(logger, Logger))
        self.assertTrue(isinstance(logger, LoggerBase))
        self.assertTrue(isinstance(logger, ServiceBase))

        self.assertEqual(logger._app_runtime, self._app_host.application_runtime)

    def test_add_scoped(self):
        print(f'{__name__}.test_add_scoped:')
        self._check_general_requirements()
        self._add_logger()

        self._services.add_scoped(PublisherBase, Publisher)

    def test_get_scoped(self):
        print(f'{__name__}.test_get_scoped:')
        self._check_general_requirements()
        self._add_logger()

        self._services.add_scoped(PublisherBase, Publisher)
        publisher: Publisher = self._services.get_service(PublisherBase)
        self.assertIsNotNone(publisher)
        self.assertTrue(isinstance(publisher, Publisher))
        self.assertTrue(isinstance(publisher, PublisherBase))
        self.assertTrue(isinstance(publisher, ServiceBase))

        self.assertTrue(isinstance(publisher._logger, Logger))
        self.assertTrue(isinstance(publisher._logger, LoggerBase))
        self.assertTrue(isinstance(publisher._logger, ServiceBase))

    def test_add_transient(self):
        print(f'{__name__}.test_add_transient:')
        self._check_general_requirements()
        self._add_logger()

        self._services.add_transient(PublisherBase, Publisher)
        self.assertGreater(len(self._services._transient_services), 0)

        self.assertTrue(bool(isinstance(service, ServiceBase) for service in self._services._transient_services))

    def test_get_transient(self):
        print(f'{__name__}.test_get_transient:')
        self._check_general_requirements()
        self._add_logger()

        self._services.add_transient(PublisherBase, Publisher)
        publisher: Publisher = self._services.get_service(PublisherBase)
        self.assertIsNotNone(publisher)
        self.assertTrue(isinstance(publisher, Publisher))
        self.assertTrue(isinstance(publisher, PublisherBase))
        self.assertTrue(isinstance(publisher, ServiceBase))

        self.assertTrue(isinstance(publisher._logger, Logger))
        self.assertTrue(isinstance(publisher._logger, LoggerBase))
        self.assertTrue(isinstance(publisher._logger, ServiceBase))
