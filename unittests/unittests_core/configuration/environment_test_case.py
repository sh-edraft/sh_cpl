import os
import unittest
from _socket import gethostname

from cpl_core.configuration import Configuration
from cpl_core.environment import ApplicationEnvironment, ApplicationEnvironmentABC
from cpl_core.environment import application_environment


class EnvironmentTestCase(unittest.TestCase):
    def setUp(self):
        self._config = Configuration()
        self._env = self._config.environment

    def test_app_env_created(self):
        self.assertTrue(isinstance(self._env, ApplicationEnvironment))
        self.assertTrue(issubclass(type(self._env), ApplicationEnvironmentABC))

    def test_app_env_values_correct_when_default(self):
        self.assertEqual(self._env.environment_name, "production")
        self.assertEqual(self._env.application_name, "")
        self.assertEqual(self._env.customer, "")
        self.assertEqual(self._env.host_name, gethostname())
        self.assertEqual(self._env.working_directory, os.getcwd())
        self.assertEqual(
            self._env.runtime_directory,
            os.path.dirname(os.path.dirname(os.path.abspath(application_environment.__file__))),
        )

    def test_app_env_values_correct_when_read_from_env(self):
        os.environ["CPLT_ENVIRONMENT"] = "development"
        os.environ["CPLT_NAME"] = "Core Tests"
        os.environ["CPLT_CUSTOMER"] = "sh-edraft.de"

        self._config.add_environment_variables("CPLT_")

        self.assertEqual(self._env.environment_name, "development")
        self.assertEqual(self._env.application_name, "Core Tests")
        self.assertEqual(self._env.customer, "sh-edraft.de")
        self.assertEqual(self._env.host_name, gethostname())
        self.assertEqual(self._env.working_directory, os.getcwd())
        self.assertEqual(
            self._env.runtime_directory,
            os.path.dirname(os.path.dirname(os.path.abspath(application_environment.__file__))),
        )

    def test_app_env_set_dirs(self):
        new_cwd = os.path.join(os.getcwd(), "../")
        self._env.set_working_directory(new_cwd)
        self.assertEqual(self._env.working_directory, new_cwd)
        self._env.set_runtime_directory(new_cwd)
        self.assertEqual(self._env.runtime_directory, new_cwd)
