import os
import unittest
from typing import cast

from sh_edraft.configuration import Configuration
from sh_edraft.environment.model import EnvironmentName
from sh_edraft.hosting import ApplicationHost
from sh_edraft.logging.model import LoggingSettings, LoggingLevel
from sh_edraft.publishing.model import PublishSettings
from sh_edraft.time.model import TimeFormatSettings


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self._app_host = ApplicationHost()
        self._config = cast(Configuration, self._app_host.configuration)

    def test_create(self):
        print(f'{__name__}.test_create:')
        self.assertIsNotNone(self._config)
        self._config.create()
        self.assertIsNotNone(self._config)

        self.assertEqual(len(self._config._config), 0)
        self.assertIsNotNone(self._app_host.application_runtime)

    def test_env_vars(self):
        print(f'{__name__}.test_env_vars:')
        self._config.add_environment_variables('PYTHON_')
        self._config.add_environment_variables('CPL_')

    def test_arguments(self):
        print(f'{__name__}.test_arguments:')
        self._config.add_argument_variables()
        self.assertEqual(self._config.environment.environment_name, EnvironmentName.testing.value)

    def test_appsettings(self):
        print(f'{__name__}.test_appsettings:')
        self._config.add_json_file(f'appsettings.json')

        time_formats: TimeFormatSettings = cast(TimeFormatSettings, self._config.get_configuration(TimeFormatSettings))
        self.assertIsNotNone(time_formats)
        self.assertEqual(time_formats.date_format, '%Y-%m-%d')
        self.assertEqual(time_formats.time_format, '%H:%M:%S')
        self.assertEqual(time_formats.date_time_format, '%Y-%m-%d %H:%M:%S.%f')
        self.assertEqual(time_formats.date_time_log_format, '%Y-%m-%d_%H-%M-%S')

        logging = cast(LoggingSettings, self._config.get_configuration(LoggingSettings))
        self.assertIsNotNone(logging)
        self.assertEqual(logging.path, 'logs/')
        self.assertEqual(logging.filename, 'log_$start_time.log')
        self.assertEqual(logging.console.value, LoggingLevel.ERROR.value)
        self.assertEqual(logging.level.value, LoggingLevel.WARN.value)

        with self.assertRaises(Exception):
            publish: PublishSettings = cast(PublishSettings, self._config.get_configuration(PublishSettings))

    def test_appsettings_environment(self):
        print(f'{__name__}.test_appsettings_environment:')
        self._config.add_argument_variables()
        self._config.add_json_file(f'appsettings.{self._config.environment.environment_name}.json')

        logging = cast(LoggingSettings, self._config.get_configuration(LoggingSettings))
        self.assertIsNotNone(logging)
        self.assertEqual(logging.path, 'logs/')
        self.assertEqual(logging.filename, 'log_$start_time.log')
        self.assertEqual(logging.console.value, LoggingLevel.TRACE.value)
        self.assertEqual(logging.level.value, LoggingLevel.TRACE.value)

        publish: PublishSettings = cast(PublishSettings, self._config.get_configuration(PublishSettings))
        self.assertIsNotNone(publish)
        self.assertEqual(publish.source_path, '../')
        self.assertEqual(publish.dist_path, '../../dist')
        self.assertEqual(publish.templates, [])
        self.assertEqual(publish.included_files, [])
        self.assertEqual(publish.excluded_files, [])
        self.assertEqual(publish.template_ending, '_template.txt')

    def test_appsettings_host(self):
        print(f'{__name__}.test_appsettings_host:')
        self._config.add_json_file(f'appsettings.{self._config.environment.host_name}.json')

    def test_appsettings_customer(self):
        print(f'{__name__}.test_appsettings_customer:')
        file_name = f'appsettings.{self._config.environment.customer}.json'
        with self.assertRaises(SystemExit):
            if os.path.isfile(f'{self._config.environment.content_root_path}/{file_name}'):
                os.remove(f'{self._config.environment.content_root_path}/{file_name}')

            self._config.add_json_file(file_name)

        self._config.add_json_file(file_name, optional=True)
