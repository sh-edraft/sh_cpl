import unittest
import datetime

from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationRuntimeBase
from sh_edraft.service.base import ServiceProviderBase


class AppHostTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_create(self):
        print(f'{__name__}.test_create:')
        app_host = ApplicationHost()
        self.assertIsNotNone(app_host)
        app_host.create()

        self.assertIsNotNone(app_host.configuration)
        self.assertTrue(isinstance(app_host.configuration, ConfigurationBase))

        self.assertIsNotNone(app_host.application_runtime)
        self.assertTrue(isinstance(app_host.application_runtime, ApplicationRuntimeBase))

        self.assertIsNotNone(app_host.services)
        self.assertTrue(isinstance(app_host.services, ServiceProviderBase))

        self.assertIsNotNone(app_host._start_time)
        self.assertTrue(isinstance(app_host._start_time, datetime.datetime))
        self.assertIsNotNone(app_host._end_time)
        self.assertTrue(isinstance(app_host._end_time, datetime.datetime))
