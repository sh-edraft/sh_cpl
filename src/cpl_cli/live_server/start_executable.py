import os
import subprocess
import sys
from datetime import datetime

from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.configuration.build_settings import BuildSettings


class StartExecutable:
    def __init__(self, env: ApplicationEnvironmentABC, build_settings: BuildSettings):
        """
        Service to start the CPL project for the live development server
        :param env:
        :param build_settings:
        """

        self._executable = None

        self._env = env
        self._build_settings = build_settings

        self._main = ""
        self._command = []
        self._env_vars = os.environ

        self._set_venv()

    def _set_venv(self):
        if self._executable is None or self._executable == sys.executable:
            return

        path = os.path.abspath(os.path.dirname(os.path.dirname(self._executable)))
        if sys.platform == "win32":
            self._env_vars["PATH"] = f"{path}\\bin" + os.pathsep + os.environ.get("PATH", "")
        else:
            self._env_vars["PATH"] = f"{path}/bin" + os.pathsep + os.environ.get("PATH", "")

        self._env_vars["VIRTUAL_ENV"] = path

    def run(self, args: list[str], executable: str, path: str, output=True):
        self._executable = os.path.abspath(os.path.join(self._env.working_directory, executable))
        if not os.path.exists(self._executable):
            Console.error(f"Executable not found")
            return

        main = self._build_settings.main
        if "." in self._build_settings.main:
            length = len(self._build_settings.main.split(".")) - 1
            main = self._build_settings.main.split(".")[length]

        self._main = os.path.join(path, f"{main}.py")
        if not os.path.isfile(self._main):
            Console.error("Entry point main.py not found")
            return

        # set cwd to src/
        self._env.set_working_directory(os.path.abspath(os.path.join(path)))
        src_cwd = os.path.abspath(os.path.join(path, "../"))
        if sys.platform == "win32":
            self._env_vars["PYTHONPATH"] = (
                f"{src_cwd};" f"{os.path.join(self._env.working_directory, self._build_settings.source_path)}"
            )
        else:
            self._env_vars["PYTHONPATH"] = (
                f"{src_cwd}:" f"{os.path.join(self._env.working_directory, self._build_settings.source_path)}"
            )

        if output:
            Console.set_foreground_color(ForegroundColorEnum.green)
            Console.write_line("Read successfully")
            Console.set_foreground_color(ForegroundColorEnum.cyan)
            Console.write_line(f'Started at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
            Console.set_foreground_color(ForegroundColorEnum.default)

        self._command = [self._executable, self._main]
        # if len(self._args) > 0:
        #     self._command.append(' '.join(self._args))
        for arg in args:
            self._command.append(arg)

        subprocess.run(self._command, env=self._env_vars)
