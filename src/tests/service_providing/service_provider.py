import unittest

from sh_edraft.configuration import ApplicationHost
from sh_edraft.configuration.model.application_host_base import ApplicationHostBase
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.publishing import Publisher
from sh_edraft.publishing.base import PublisherBase
from sh_edraft.publishing.model.publish_settings_model import PublishSettingsModel
from sh_edraft.service import ServiceProvider
from sh_edraft.service.base import ServiceBase
from sh_edraft.time.model import TimeFormatSettings


class ServiceProviderTest(unittest.TestCase):

    def setUp(self):
        self._app_host = ApplicationHost()
        self._services = self._app_host.services
        self._services.create()

        self._log_settings = LoggingSettings()
        self._log_settings.from_dict({
            "Path": "logs/",
            "Filename": "log_$start_time.log",
            "ConsoleLogLevel": "TRACE",
            "FileLogLevel": "TRACE"
        })
        self._services.config.add_config_by_type(LoggingSettings, self._log_settings)

        self._time_format_settings = TimeFormatSettings()
        self._time_format_settings.from_dict({
            "DateFormat": "%Y-%m-%d",
            "TimeFormat": "%H:%M:%S",
            "DateTimeFormat": "%Y-%m-%d %H:%M:%S.%f",
            "DateTimeLogFormat": "%Y-%m-%d_%H-%M-%S"
        })
        self._services.config.add_config_by_type(TimeFormatSettings, self._time_format_settings)
        self._services.config.add_config_by_type(ApplicationHost, self._app_host)

        self._publish_settings_model = PublishSettingsModel()
        self._publish_settings_model.from_dict({
            "SourcePath": "../",
            "DistPath": "../../dist",
            "Templates": [],
            "IncludedFiles": [],
            "ExcludedFiles": [],
            "TemplateEnding": "_template.txt",
        })
        self._services.config.add_config_by_type(PublishSettingsModel, self._publish_settings_model)

    def _check_general_requirements(self):
        self.assertIsNotNone(self._services)

    def _add_logger(self):
        self._services.add_singleton(LoggerBase, Logger)
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()

    def test_create(self):
        print(f'{__name__}.test_create:')
        provider = ServiceProvider()
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
                    isinstance(service, Logger) and isinstance(service, LoggerBase) and isinstance(service, ServiceBase)
            ):
                if not found:
                    found = True

        self.assertTrue(found)

        found = False
        for service_type in self._services._singleton_services:
            service = self._services._singleton_services[service_type]
            if service_type == PublisherBase and (
                    isinstance(service, Publisher) and isinstance(service, PublisherBase) and isinstance(service, ServiceBase)
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

        self.assertEqual(logger._log_settings, self._log_settings)
        self.assertEqual(logger._time_format_settings, self._time_format_settings)
        self.assertEqual(logger._app_host, self._app_host)

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
