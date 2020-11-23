import os
import unittest
from string import Template

from sh_edraft.configuration import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.publish import Publisher
from sh_edraft.publish.base import PublisherBase
from sh_edraft.service.base import ServiceBase
from sh_edraft.time.model import TimeFormatSettings


class ServiceProviderServices(unittest.TestCase):

    def setUp(self):
        self._app_host = ApplicationHost()
        self._services = self._app_host.services
        self._services.init(())
        self._services.create()

        self._log_settings = LoggingSettings()
        self._log_settings.from_dict({
            "Path": "logs/",
            "Filename": "log_$start_time.log",
            "ConsoleLogLevel": "TRACE",
            "FileLogLevel": "TRACE"
        })

        self._time_format_settings = TimeFormatSettings()
        self._time_format_settings.from_dict({
            "DateFormat": "%Y-%m-%d",
            "TimeFormat": "%H:%M:%S",
            "DateTimeFormat": "%Y-%m-%d %H:%M:%S.%f",
            "DateTimeLogFormat": "%Y-%m-%d_%H-%M-%S"
        })

    def _check_general_requirements(self):
        self.assertIsNotNone(self._services)

    def _check_logger_requirements(self):
        self.assertIsNotNone(self._log_settings)
        self.assertIsNotNone(self._time_format_settings)

    def test_add_singleton(self):
        print(f'{__name__}.test_add_singleton:')
        self._check_general_requirements()
        self._check_logger_requirements()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
        self.assertGreater(len(self._services._singleton_services), 0)

        found = False
        for service in self._services._singleton_services:
            if isinstance(service, Logger) and isinstance(service, LoggerBase) and isinstance(service, ServiceBase):
                if not found:
                    found = True

        self.assertTrue(found)

    def test_get_singleton(self):
        print(f'{__name__}.test_get_singleton:')
        self._check_general_requirements()
        self._check_logger_requirements()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
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
        self._check_logger_requirements()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
        self._services.add_scoped(Publisher, self._services.get_service(LoggerBase), '../', '../../dist', [])
        self.assertGreater(len(self._services._scoped_services), 0)

    def test_get_scoped(self):
        print(f'{__name__}.test_get_scoped:')
        self._check_general_requirements()
        self._check_logger_requirements()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
        self._services.add_scoped(Publisher, self._services.get_service(LoggerBase), '../', '../../dist', [])
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
        self._check_logger_requirements()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
        self._services.add_transient(Publisher, self._services.get_service(LoggerBase), '../', '../../dist', [])
        self.assertGreater(len(self._services._transient_services), 0)

        self.assertTrue(bool(isinstance(service, ServiceBase) for service in self._services._transient_services))

    def test_get_transient(self):
        print(f'{__name__}.test_get_transient:')
        self._check_general_requirements()
        self._check_logger_requirements()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
        self._services.add_transient(Publisher, self._services.get_service(LoggerBase), '../', '../../dist', [])
        publisher: Publisher = self._services.get_service(PublisherBase)
        self.assertIsNotNone(publisher)
        self.assertTrue(isinstance(publisher, Publisher))
        self.assertTrue(isinstance(publisher, PublisherBase))
        self.assertTrue(isinstance(publisher, ServiceBase))

        self.assertTrue(isinstance(publisher._logger, Logger))
        self.assertTrue(isinstance(publisher._logger, LoggerBase))
        self.assertTrue(isinstance(publisher._logger, ServiceBase))
