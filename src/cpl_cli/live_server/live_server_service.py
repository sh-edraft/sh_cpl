import os
import time
from contextlib import suppress

import psutil as psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from cpl.console.console import Console
from cpl.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.live_server.live_server_thread import LiveServerThread


class LiveServerService(FileSystemEventHandler):

    def __init__(self, env: ApplicationEnvironmentABC, build_settings: BuildSettings):
        """
        Service for the live development server
        :param env:
        :param build_settings:
        """
        FileSystemEventHandler.__init__(self)

        self._env = env
        self._build_settings = build_settings

        self._src_dir = os.path.join(self._env.working_directory, self._build_settings.source_path)
        self._ls_thread = None
        self._observer = None

    def _start_observer(self):
        """
        Starts the file changes observer
        :return:
        """
        self._observer = Observer()
        self._observer.schedule(self, path=self._src_dir, recursive=True)
        self._observer.start()

    def _restart(self):
        """
        Restarts the CPL project
        :return:
        """
        for proc in psutil.process_iter():
            with suppress(Exception):
                if proc.cmdline() == self._ls_thread.command:
                    proc.kill()

        Console.write_line('Restart\n')
        while self._ls_thread.is_alive():
            time.sleep(1)

        self._start()

    def on_modified(self, event):
        """
        Triggers when source file is modified
        :param event:
        :return:
        """
        if event.is_directory:
            return None

        # Event is modified, you can process it now
        if str(event.src_path).endswith('.py'):
            self._observer.stop()
            self._restart()

    def _start(self):
        self._start_observer()
        self._ls_thread = LiveServerThread(self._src_dir, self._build_settings)
        self._ls_thread.start()
        self._ls_thread.join()
        Console.close()

    def start(self):
        """
        Starts the CPL live development server
        :return:
        """
        Console.write_line('** CPL live development server is running **')
        self._start()
