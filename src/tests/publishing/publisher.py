import os
import shutil
import unittest

from sh_edraft.configuration import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.publishing import Publisher
from sh_edraft.publishing.base import PublisherBase
from sh_edraft.publishing.model import Template
from sh_edraft.source_code.model import Version
from sh_edraft.time.model import TimeFormatSettings


class PublisherTest(unittest.TestCase):

    def _config(self):
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

        self._version = Version(2020, 12, 5).to_dict()
        self._templates = [
            Template(
                '../../publish_templates/*_template.txt',
                '*',
                '',
                '',
                '2020',
                'sh-edraft.de',
                'MIT',
                ', see LICENSE for more details.',
                '',
                'Sven Heidemann',
                self._version
            ),
            Template(
                '../../publish_templates/*_template.txt',
                'sh_edraft',
                'common python library',
                'Library to share common classes and models used at sh-edraft.de',
                '2020',
                'sh-edraft.de',
                'MIT',
                ', see LICENSE for more details.',
                '',
                'Sven Heidemann',
                self._version
            )
        ]

        self._source = '../'
        self._dist = '../../dist'

    def setUp(self):
        self._config()

        self._app_host = ApplicationHost()
        self._services = self._app_host.services
        self._services.init(())
        self._services.create()

        self._services.add_singleton(Logger, self._log_settings, self._time_format_settings, self._app_host)
        logger: Logger = self._services.get_service(LoggerBase)
        logger.create()

    def tearDown(self):
        if os.path.isdir(self._log_settings.path):
            shutil.rmtree(self._log_settings.path)

    def test_create(self):
        self._services.add_transient(Publisher, self._services.get_service(LoggerBase), self._source, self._dist, self._templates)
        publisher: Publisher = self._services.get_service(PublisherBase)
        self.assertIsNotNone(publisher)

        publisher.create()
        self.assertTrue(os.path.isdir(self._dist))
