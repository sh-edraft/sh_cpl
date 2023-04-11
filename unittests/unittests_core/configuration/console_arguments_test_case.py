import sys
import unittest
from unittest.mock import Mock, MagicMock

from cpl_core.configuration import Configuration, ArgumentTypeEnum
from cpl_core.dependency_injection import ServiceCollection


class ConsoleArgumentsTestCase(unittest.TestCase):
    def setUp(self):
        self._config = Configuration()

        self._config.create_console_argument(ArgumentTypeEnum.Flag, "", "flag", [])
        self._config.create_console_argument(ArgumentTypeEnum.Variable, "", "var", [], "=")

        self._config.create_console_argument(ArgumentTypeEnum.Executable, "", "exec", [], Mock).add_console_argument(
            ArgumentTypeEnum.Flag, "--", "dev", ["d", "D"]
        ).add_console_argument(ArgumentTypeEnum.Flag, "--", "virtual", ["v", "V"]).add_console_argument(
            ArgumentTypeEnum.Variable, "", "var1", [], "="
        )

        self._config.for_each_argument(
            lambda a: a.add_console_argument(ArgumentTypeEnum.Flag, "--", "help", ["h", "H"])
        )

        self._sc = ServiceCollection(self._config)
        self._mocked_exec = Mock()
        self._mocked_exec.run = MagicMock()
        self._sc.add_transient(self._mocked_exec)

    def test_flag(self):
        sys.argv.append("flag")

        self._config.parse_console_arguments(self._sc.build_service_provider())
        self.assertIn("flag", self._config.additional_arguments)

    def test_var(self):
        sys.argv.append("var=1")
        sys.argv.append("var2=1")

        self._config.parse_console_arguments(self._sc.build_service_provider())
        self.assertEqual("1", self._config.get_configuration("var"))
        self.assertIsNone(self._config.get_configuration("var1"))

    def test_exec(self):
        sys.argv.append("exec")

        self._config.parse_console_arguments(self._sc.build_service_provider())
        self._mocked_exec.run.assert_called()

    def test_exec_with_one_flag(self):
        sys.argv.append("exec")
        sys.argv.append("--dev")

        self._config.parse_console_arguments(self._sc.build_service_provider())
        self._mocked_exec.run.assert_called()
        self.assertIn("dev", self._config.additional_arguments)

    def test_exec_with_one_flag_alias(self):
        sys.argv.append("exec")
        sys.argv.append("--d")

        self._config.parse_console_arguments(self._sc.build_service_provider())
        self._mocked_exec.run.assert_called()
        self.assertIn("dev", self._config.additional_arguments)

    def test_exec_with_two_flags(self):
        sys.argv.append("exec")
        sys.argv.append("--dev")
        sys.argv.append("--virtual")

        self._config.parse_console_arguments(self._sc.build_service_provider())
        self._mocked_exec.run.assert_called()
        self.assertIn("dev", self._config.additional_arguments)
        self.assertIn("virtual", self._config.additional_arguments)
