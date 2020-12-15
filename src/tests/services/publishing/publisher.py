import os
import shutil
import unittest

from sh_edraft.hosting import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.model import LoggingSettings
from sh_edraft.publishing import Publisher
from sh_edraft.publishing.model import Template
from sh_edraft.publishing.model import PublishSettings
from sh_edraft.coding.model import Version
from sh_edraft.time.model import TimeFormatSettings


class PublisherTest(unittest.TestCase):

    def _configure(self):
        self._version = Version(2020, 12, 5)
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

        self._publish_settings_model = PublishSettings()
        self._publish_settings_model.from_dict({
            "SourcePath": self._source_path,
            "DistPath": self._dist_path,
            "Templates": templates,
            "IncludedFiles": [],
            "ExcludedFiles": [],
            "TemplateEnding": "_template.txt",
        })

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

        self._app_runtime = self._app_host.application_runtime

        self._configure()

        self._log_settings: LoggingSettings = self._config.get_configuration(LoggingSettings)
        self._time_format_settings: TimeFormatSettings = self._config.get_configuration(TimeFormatSettings)
        self._logger = Logger(self._log_settings, self._time_format_settings, self._app_host.application_runtime)
        self._logger.create()

    def tearDown(self):
        if os.path.isdir(self._log_settings.path):
            shutil.rmtree(self._log_settings.path)

    def test_create(self):
        print(f'{__name__}.test_create:')
        publisher: Publisher = Publisher(self._logger, self._publish_settings_model)
        self.assertIsNotNone(publisher)

        publisher.create()
        self.assertTrue(os.path.isdir(self._dist_path))
        self.assertEqual(publisher._publish_settings, self._publish_settings_model)
