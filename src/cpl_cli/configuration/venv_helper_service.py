import os
import subprocess
import sys

from cpl_cli.configuration import ProjectSettings
from cpl_core.environment import ApplicationEnvironmentABC

from cpl_core.utils import Pip

from cpl_core.console import Console, ForegroundColorEnum


class VenvHelper:
    @staticmethod
    def init_venv(
        is_virtual: bool, env: ApplicationEnvironmentABC, project_settings: ProjectSettings, explicit_path=None
    ):
        if is_virtual:
            return

        venv_path = os.path.abspath(os.path.join(env.working_directory, project_settings.python_executable, "../../"))

        if explicit_path is not None:
            venv_path = os.path.abspath(explicit_path)

        if not os.path.exists(venv_path):
            Console.spinner(
                f"Creating venv: {venv_path}",
                VenvHelper.create_venv,
                venv_path,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan,
            )

        Pip.set_executable(project_settings.python_executable)

    @staticmethod
    def create_venv(path):
        subprocess.run(
            [sys.executable, "-m", "venv", os.path.abspath(os.path.join(path, "../../"))],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
