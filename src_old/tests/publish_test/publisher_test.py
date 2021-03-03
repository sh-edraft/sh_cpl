import os
import unittest

from sh_edraft.console import Console
from sh_edraft.hosting import ApplicationHost
from sh_edraft.logging import Logger
from sh_edraft.logging.base import LoggerBase
from sh_edraft.publish import Publisher
from sh_edraft.publish.base import PublisherBase
from sh_edraft.publish.model import PublishSettings


class PublisherTest(unittest.TestCase):

    def setUp(self):
        Console.disable()
        self._app_host = ApplicationHost()
        self._configuration = self._app_host.configuration
        self._services = self._app_host.services

        self._configuration.add_environment_variables('CPL_')
        self._configuration.add_argument_variables()
        self._configuration.add_json_file(f'build.json')

        self._services.add_singleton(LoggerBase, Logger)
        self._services.add_singleton(PublisherBase, Publisher)
        self._publisher: Publisher = self._services.get_service(PublisherBase)

    def test_include(self):
        value = './test.py'
        self._publisher.include(value)
        self.assertTrue(value in self._publisher._publish_settings.included_files)

    def test_exclude(self):
        value = './test.py'
        self._publisher.exclude(value)
        self.assertTrue(value in self._publisher._publish_settings.excluded_files)

    def test_create(self):
        self._publisher.create()
        self.assertTrue(os.path.isdir(self._configuration.get_configuration(PublishSettings).dist_path))

    def test_build(self):
        self._publisher.create()
        self._publisher.build()
        self.assertTrue(os.path.isdir(self._configuration.get_configuration(PublishSettings).dist_path))

    def test_publish(self):
        self._publisher.create()
        self._publisher.build()
        self._publisher.publish()
        self.assertTrue(os.path.isdir(self._configuration.get_configuration(PublishSettings).dist_path))
