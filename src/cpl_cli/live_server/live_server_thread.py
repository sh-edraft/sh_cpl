import os
import subprocess
import sys
import threading
from datetime import datetime

from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl_cli.configuration import BuildSettings


class LiveServerThread(threading.Thread):

    def __init__(self, path: str, build_settings: BuildSettings, args: list[str]):
        """
        Thread to start the CPL project for the live development server
        :param path:
        """
        threading.Thread.__init__(self)

        self._path = path
        self._build_settings = build_settings
        self._args = args

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
        src_path = ''
        main = self._build_settings.main
        if '.' in self._build_settings.main:
            length = len(self._build_settings.main.split('.')) - 1
            src_path = self._path.replace(f'{"/".join(self._build_settings.main.split(".")[:length])}/', '')
            main = self._build_settings.main.split('.')[length]

        self._main = os.path.join(self._path, f'{main}.py')
        if not os.path.isfile(self._main):
            Console.error('Entry point main.py not found')
            return

        env_vars = os.environ
        if sys.platform == 'win32':
            env_vars['PYTHONPATH'] = f'{os.path.dirname(src_path)};' \
                                     f'{os.path.join(os.path.dirname(src_path), self._build_settings.source_path)}'
        else:
            env_vars['PYTHONPATH'] = f'{os.path.dirname(src_path)}:' \
                                     f'{os.path.join(os.path.dirname(src_path), self._build_settings.source_path)}'

        Console.set_foreground_color(ForegroundColorEnum.green)
        Console.write_line('Read successfully')
        Console.set_foreground_color(ForegroundColorEnum.cyan)
        now = datetime.now()
        Console.write_line(f'Started at {now.strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        Console.set_foreground_color(ForegroundColorEnum.default)

        self._command = [sys.executable, self._main, ''.join(self._args)]
        subprocess.run(self._command, env=env_vars)
