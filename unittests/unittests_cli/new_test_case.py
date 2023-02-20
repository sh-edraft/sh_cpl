import json
import os
import unittest

from cpl_core.utils import String
from unittests_cli.abc.command_test_case import CommandTestCase
from unittests_cli.constants import PLAYGROUND_PATH
from unittests_shared.cli_commands import CLICommands


class NewTestCase(CommandTestCase):
    def __init__(self, method_name: str):
        CommandTestCase.__init__(self, method_name)

    def _test_project(self, project_type: str, name: str, *args, test_venv=False, without_ws=False):
        CLICommands.new(project_type, name, *args, output=False)
        workspace_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, name))
        self.assertTrue(os.path.exists(workspace_path))
        if test_venv:
            with self.subTest(msg="Venv exists"):
                self.assertTrue(os.path.exists(os.path.join(workspace_path, "venv")))
                self.assertTrue(os.path.exists(os.path.join(workspace_path, "venv/bin")))
                self.assertTrue(os.path.exists(os.path.join(workspace_path, "venv/bin/python")))
                self.assertTrue(os.path.islink(os.path.join(workspace_path, "venv/bin/python")))

        base = "src"
        if "--base" in args and "/" in name:
            base = name.split("/")[0]
            name = name.replace(f'{name.split("/")[0]}/', "")

        project_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, name, base, String.convert_to_snake_case(name)))
        if without_ws:
            project_path = os.path.abspath(
                os.path.join(PLAYGROUND_PATH, base, name, "src/", String.convert_to_snake_case(name))
            )

        with self.subTest(msg="Project json exists"):
            self.assertTrue(os.path.exists(project_path))
            self.assertTrue(os.path.exists(os.path.join(project_path, f"{name}.json")))

        if project_type == "library":
            with self.subTest(msg="Library class1 exists"):
                self.assertTrue(os.path.exists(os.path.join(project_path, f"class1.py")))
            return

        with self.subTest(msg="Project main.py exists"):
            self.assertTrue(os.path.exists(os.path.join(project_path, f"main.py")))

        with self.subTest(msg="Application base"):
            if "--ab" in args:
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"application.py")))
            else:
                self.assertFalse(os.path.isfile(os.path.join(project_path, f"application.py")))

        # s depends on ab
        with self.subTest(msg="Startup"):
            if "--ab" in args and "--s" in args:
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"startup.py")))
            else:
                self.assertFalse(os.path.isfile(os.path.join(project_path, f"startup.py")))

        with self.subTest(msg="Unittest"):
            if project_type == "unittest":
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"test_case.py")))
            else:
                self.assertFalse(os.path.isfile(os.path.join(project_path, f"test_case.py")))

        with self.subTest(msg="Discord"):
            if project_type == "discord-bot":
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"events/__init__.py")))
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"events/on_ready_event.py")))
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"commands/__init__.py")))
                self.assertTrue(os.path.isfile(os.path.join(project_path, f"commands/ping_command.py")))
            else:
                self.assertFalse(os.path.isfile(os.path.join(project_path, f"events/on_ready_event.py")))
                self.assertFalse(os.path.isfile(os.path.join(project_path, f"commands/ping_command.py")))

    def _test_sub_project(self, project_type: str, name: str, workspace_name: str, *args, test_venv=False):
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), workspace_name)))
        CLICommands.new(project_type, name, *args)
        workspace_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, workspace_name))
        self.assertTrue(os.path.exists(workspace_path))
        if test_venv:
            self.assertTrue(os.path.exists(os.path.join(workspace_path, "venv")))
            self.assertTrue(os.path.exists(os.path.join(workspace_path, "venv/bin")))
            self.assertTrue(os.path.exists(os.path.join(workspace_path, "venv/bin/python")))
            self.assertTrue(os.path.islink(os.path.join(workspace_path, "venv/bin/python")))

        base = "src"
        if "--base" in args and "/" in name:
            base = name.split("/")[0]
            name = name.replace(f'{name.split("/")[0]}/', "")

        project_path = os.path.abspath(
            os.path.join(PLAYGROUND_PATH, workspace_name, base, String.convert_to_snake_case(name))
        )
        self.assertTrue(os.path.exists(project_path))
        self.assertTrue(os.path.join(project_path, f"{name}.json"))

        if project_type == "discord-bot":
            self.assertTrue(os.path.isfile(os.path.join(project_path, f"events/__init__.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_path, f"events/on_ready_event.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_path, f"commands/__init__.py")))
            self.assertTrue(os.path.isfile(os.path.join(project_path, f"commands/ping_command.py")))
        else:
            self.assertFalse(os.path.isfile(os.path.join(project_path, f"events/on_ready_event.py")))
            self.assertFalse(os.path.isfile(os.path.join(project_path, f"commands/ping_command.py")))

    def _test_sub_directory_project(self, project_type: str, directory: str, name: str, workspace_name: str, *args):
        os.chdir(os.path.abspath(os.path.join(os.getcwd(), workspace_name)))
        CLICommands.new(project_type, f"{directory}/{name}", *args)
        workspace_path = os.path.abspath(os.path.join(PLAYGROUND_PATH, workspace_name))
        self.assertTrue(os.path.exists(workspace_path))

        project_path = os.path.abspath(
            os.path.join(PLAYGROUND_PATH, workspace_name, f"src/{directory}", String.convert_to_snake_case(name))
        )
        self.assertTrue(os.path.exists(project_path))
        project_file = os.path.join(project_path, f"{name}.json")
        self.assertTrue(os.path.exists(project_file))
        with open(project_file, "r", encoding="utf-8") as cfg:
            # load json
            project_json = json.load(cfg)
            cfg.close()

        project_settings = project_json["ProjectSettings"]
        build_settings = project_json["BuildSettings"]

        self.assertEqual(project_settings["Name"], name)
        self.assertEqual(build_settings["ProjectType"], "library")
        self.assertEqual(build_settings["OutputPath"], "../../dist")
        self.assertEqual(build_settings["Main"], f"{String.convert_to_snake_case(name)}.main")
        self.assertEqual(build_settings["EntryPoint"], name)

    def test_console(self):
        self._test_project("console", "test-console", "--ab", "--s", "--venv", test_venv=True)

    def test_console_with_other_base(self):
        self._test_project(
            "console", "tools/test-console", "--ab", "--s", "--venv", "--base", test_venv=True, without_ws=True
        )

    def test_console_without_s(self):
        self._test_project("console", "test-console-without-s", "--ab")

    def test_console_without_ab(self):
        self._test_project("console", "test-console-without-ab", "--sp")

    def test_console_without_anything(self):
        self._test_project("console", "test-console-without-anything", "--n")

    def test_console_sub(self):
        self._test_sub_project(
            "console", "test-sub-console", "test-console", "--ab", "--s", "--sp", "--venv", test_venv=True
        )

    def test_console_sub_with_other_base(self):
        self._test_sub_project(
            "console",
            "tools/test-sub-console",
            "test-console",
            "--ab",
            "--s",
            "--sp",
            "--venv",
            "--base",
            test_venv=True,
        )

    def test_discord_bot(self):
        self._test_project("discord-bot", "test-bot", "--ab", "--s", "--venv", test_venv=True)

    def test_discord_bot_sub(self):
        self._test_sub_project("discord-bot", "test-bot-sub", "test-console", "--ab", "--s", "--venv", test_venv=True)

    def test_library(self):
        self._test_project("library", "test-library", "--ab", "--s", "--sp")

    def test_library_sub(self):
        self._test_sub_project("library", "test-sub-library", "test-console", "--ab", "--s", "--sp")

    def test_library_sub_directory(self):
        self._test_sub_directory_project(
            "library", "directory", "test-sub-library", "test-console", "--ab", "--s", "--sp"
        )

    def test_unittest(self):
        self._test_project("unittest", "test-unittest", "--ab")

    def test_unittest_sub(self):
        self._test_sub_project("unittest", "test-unittest", "test-console", "--ab", "--s", "--sp")
