import os
import unittest

from cpl_core.configuration import Configuration
from cpl_core.database import DatabaseSettings
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
