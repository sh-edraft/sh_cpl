import os
import signal
import subprocess
import time

import psutil as psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from cpl.application import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration import BuildSettings
from cpl_cli.live_server.live_server import LiveServerThread


class StartService(CommandABC, FileSystemEventHandler):

    def __init__(self, runtime: ApplicationRuntimeABC, build_settings: BuildSettings):
        CommandABC.__init__(self)
        FileSystemEventHandler.__init__(self)

        self._runtime = runtime
        self._build_settings = build_settings

        self._src_dir = os.path.join(self._runtime.working_directory, self._build_settings.source_path)
        self._live_server = LiveServerThread(self._src_dir)
        self._observer = None

    def _start_observer(self):
        self._observer = Observer()
        self._observer.schedule(self, path=self._src_dir, recursive=True)
        self._observer.start()

    def _restart(self):
        for proc in psutil.process_iter():
            try:
                if proc.cmdline() == self._live_server.command:
                    os.system(f'pkill -f {self._live_server.main}')
            except Exception as e:
                pass

        Console.write_line('Restart\n')

        while self._live_server.is_alive():
            time.sleep(1)

        self._live_server = LiveServerThread(self._src_dir)
        self._live_server.start()

        self._start_observer()

    def on_modified(self, event):
        if event.is_directory:
            return None

        # Event is modified, you can process it now
        if str(event.src_path).endswith('.py'):
            self._observer.stop()
            self._restart()

    def run(self, args: list[str]):
        Console.write_line('** CPL live development server is running **')
        self._start_observer()
        self._live_server.start()

        Console.close()
        Console.write('\n')
