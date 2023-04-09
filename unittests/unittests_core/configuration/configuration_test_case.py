import os
import sys
import unittest
from unittest.mock import Mock, MagicMock

from cpl_core.configuration import Configuration, ArgumentTypeEnum
from cpl_core.database import DatabaseSettings
from cpl_core.dependency_injection import ServiceProvider, ServiceCollection
from cpl_core.mailing import EMailClientSettings


class ConfigurationTestCase(unittest.TestCase):
    def setUp(self):
        self._config = Configuration()

    def test_env_vars(self):
        os.environ["CPLT_TESTVAR"] = "Hello World"
        os.environ["CPL_NOT_EXISTING"] = "Hello World"

        self._config.add_environment_variables("CPLT_")

        self.assertEqual(self._config.get_configuration("TESTVAR"), "Hello World")
        self.assertEqual(self._config.get_configuration("TESTVAR"), "Hello World")
        self.assertEqual(self._config.get_configuration("NOT_EXISTING"), None)

    def test_add_json_file(self):
        self._config.add_json_file("unittests_core/configuration/test-settings.json")
        db = self._config.get_configuration(DatabaseSettings)
        self.assertIsNotNone(db)
        self.assertEqual("localhost", db.host)
        self.assertEqual("local", db.user)
        self.assertEqual("bG9jYWw=", db.password)
        self.assertEqual("local", db.database)
        self.assertEqual(int, type(db.port))
        self.assertEqual(3306, db.port)
        self.assertEqual("utf8mb4", db.charset)
        self.assertTrue(db.use_unicode)
        self.assertTrue(db.buffered)
        self.assertEqual("mysql_native_password", db.auth_plugin)
        self.assertIsNone(self._config.get_configuration(EMailClientSettings))

    def test_add_config(self):
        self.assertIsNone(self._config.get_configuration("Test"))
        self._config.add_configuration("Test", "Hello World")
        self.assertIsNotNone(self._config.get_configuration("Test"))
        self.assertEqual("Hello World", self._config.get_configuration("Test"))

    def test_console_argument(self):
        sc = ServiceCollection(self._config)
        self.assertEqual([], sys.argv[1:])
        sys.argv.append("flag")
        sys.argv.append("exec")
        sys.argv.append("var=test")
        self.assertNotEqual([], sys.argv[1:])

        self._config.create_console_argument(ArgumentTypeEnum.Flag, "", "flag", [])
        mocked_exec = Mock()
        mocked_exec.run = MagicMock()
        sc.add_transient(mocked_exec)
        self._config.create_console_argument(ArgumentTypeEnum.Executable, "", "exec", [], Mock)
        self._config.create_console_argument(ArgumentTypeEnum.Variable, "", "var", [], "=")

        self.assertIsNone(self._config.get_configuration("var"))
        self._config.parse_console_arguments(sc.build_service_provider())
        mocked_exec.run.assert_called()

        self.assertEqual("test", self._config.get_configuration("var"))
        self.assertIn("flag", self._config.additional_arguments)
