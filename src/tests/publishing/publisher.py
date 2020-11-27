import os
import shutil
import unittest

from sh_edraft.hosting import ApplicationHost, HostingEnvironment
from sh_edraft.hosting.model import EnvironmentName
from sh_edraft.logging import Logger
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.publishing import Publisher
from sh_edraft.publishing.model import Template
from sh_edraft.publishing.model import PublishSettingsModel
from sh_edraft.coding.model import Version
from sh_edraft.time.model import TimeFormatSettings


class PublisherTest(unittest.TestCase):

    def _configure(self):
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
        templates = [
            Template(
                '../../publish_templates/all_template.txt',
                'all',
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
                '../../publish_templates/all_template.txt',
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

        self._source_path = '../'
        self._dist_path = '../../dist'

        self._publish_settings_model = PublishSettingsModel()
        self._publish_settings_model.from_dict({
            "SourcePath": self._source_path,
            "DistPath": self._dist_path,
            "Templates": templates,
            "IncludedFiles": [],
            "ExcludedFiles": [],
            "TemplateEnding": "_template.txt",
        })

    def setUp(self):
        self._configure()

        app_host = ApplicationHost('CPL_Test')
        self._app_runtime = app_host.application_runtime

        self._logger = Logger(self._log_settings, self._time_format_settings, app_host.application_runtime)
        self._logger.create()

    def tearDown(self):
        if os.path.isdir(self._log_settings.path):
            shutil.rmtree(self._log_settings.path)

    def test_create(self):
        publisher: Publisher = Publisher(self._logger, self._publish_settings_model)
        self.assertIsNotNone(publisher)

        publisher.create()
        self.assertTrue(os.path.isdir(self._dist_path))
        self.assertEqual(publisher._publish_settings, self._publish_settings_model)
