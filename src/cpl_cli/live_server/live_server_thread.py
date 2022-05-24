import os
import subprocess
import sys
import threading
from datetime import datetime

from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.configuration import BuildSettings


class LiveServerThread(threading.Thread):

    def __init__(self, executable: str, path: str, args: list[str], env: ApplicationEnvironmentABC,
                 build_settings: BuildSettings):
        """
        Thread to start the CPL project for the live development server
        :param executable:
        :param path:
        :param args:
        :param env:
        :param build_settings:
        """
        threading.Thread.__init__(self)

        self._executable = os.path.abspath(executable)

        self._path = path
        self._args = args
        self._env = env
        self._build_settings = build_settings

        self._main = ''
        self._command = []
        self._env_vars = os.environ

        self._set_venv()

    @property
    def command(self) -> list[str]:
        return self._command

    @property
    def main(self) -> str:
        return self._main

    def _set_venv(self):
        if self._executable != sys.executable:
            path = os.path.abspath(os.path.dirname(os.path.dirname(self._executable)))
            if sys.platform == 'win32':
                self._env_vars['PATH'] = f'{path}\\bin' + os.pathsep + os.environ.get('PATH', '')
            else:
                self._env_vars['PATH'] = f'{path}/bin' + os.pathsep + os.environ.get('PATH', '')

            self._env_vars['VIRTUAL_ENV'] = path

    def run(self):
        """
        Starts the CPL project
        :return:
        """
        main = self._build_settings.main
        if '.' in self._build_settings.main:
            length = len(self._build_settings.main.split('.')) - 1
            main = self._build_settings.main.split('.')[length]

        self._main = os.path.join(self._path, f'{main}.py')
        if not os.path.isfile(self._main):
            Console.error('Entry point main.py not found')
            return

        # set cwd to src/
        self._env.set_working_directory(os.path.abspath(os.path.join(self._path)))
        src_cwd = os.path.abspath(os.path.join(self._path, '../'))
        if sys.platform == 'win32':
            self._env_vars['PYTHONPATH'] = f'{src_cwd};' \
                                           f'{os.path.join(self._env.working_directory, self._build_settings.source_path)}'
        else:
            self._env_vars['PYTHONPATH'] = f'{src_cwd}:' \
                                           f'{os.path.join(self._env.working_directory, self._build_settings.source_path)}'

        Console.set_foreground_color(ForegroundColorEnum.green)
        Console.write_line('Read successfully')
        Console.set_foreground_color(ForegroundColorEnum.cyan)
        now = datetime.now()
        Console.write_line(f'Started at {now.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        Console.set_foreground_color(ForegroundColorEnum.default)

        self._command = [self._executable, self._main]
        # if len(self._args) > 0:
        #     self._command.append(' '.join(self._args))
        for arg in self._args:
            self._command.append(arg)

        subprocess.run(self._command, env=self._env_vars)
