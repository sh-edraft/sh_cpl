import os
import subprocess
import sys
import threading
from datetime import datetime

from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl_cli.configuration import BuildSettings


class LiveServerThread(threading.Thread):

    def __init__(self, path: str, build_settings: BuildSettings):
        """
        Thread to start the CPL project for the live development server
        :param path:
        """
        threading.Thread.__init__(self)

        self._path = path
        self._build_settings = build_settings

        self._main = ''
        self._command = []

    @property
    def command(self) -> list[str]:
        return self._command

    @property
    def main(self) -> str:
        return self._main

    def run(self):
        """
        Starts the CPL project
        :return:
        """
        main = self._build_settings.main.replace('.', '/')
        self._main = os.path.join(self._path, f'{main}.py')
        if not os.path.isfile(self._main):
            Console.error('Entry point main.py not found')
            return

        Console.set_foreground_color(ForegroundColorEnum.green)
        Console.write_line('Read successfully')
        Console.set_foreground_color(ForegroundColorEnum.cyan)
        now = datetime.now()
        Console.write_line(f'Started at {now.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        Console.set_foreground_color(ForegroundColorEnum.default)

        env_vars = os.environ
        if sys.platform == 'win32':
            env_vars['PYTHONPATH'] = f'{os.path.dirname(self._path)};' \
                                     f'{os.path.join(os.path.dirname(self._path), self._build_settings.source_path)}'
        else:
            env_vars['PYTHONPATH'] = f'{os.path.dirname(self._path)}:' \
                                     f'{os.path.join(os.path.dirname(self._path), self._build_settings.source_path)}'

        self._command = [sys.executable, self._main, ''.join(sys.argv[2:])]
        subprocess.run(self._command, env=env_vars)
