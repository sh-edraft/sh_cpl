import os
import time
from contextlib import suppress

import psutil as psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from cpl_cli.publish import PublisherService
from cpl_core.console.console import Console
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.live_server.live_server_thread import LiveServerThread
from cpl_core.utils import String


class LiveServerService(FileSystemEventHandler):
    def __init__(
        self,
        env: ApplicationEnvironmentABC,
        project_settings: ProjectSettings,
        build_settings: BuildSettings,
        publisher: PublisherService,
    ):
        """
        Service for the live development server
        :param env:
        :param project_settings:
        :param build_settings:
        """
        FileSystemEventHandler.__init__(self)

        self._env = env
        self._project_settings = project_settings
        self._build_settings = build_settings
        self._publisher = publisher

        self._src_dir = os.path.join(self._env.working_directory, self._build_settings.source_path)
        self._wd = self._src_dir
        self._ls_thread = None
        self._observer = None

        self._args: list[str] = []
        self._is_dev = False

    def _start_observer(self):
        """
        Starts the file changes observer
        :return:
        """
        self._observer = Observer()
        self._observer.schedule(self, path=os.path.abspath(os.path.join(self._src_dir, "../")), recursive=True)
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

        Console.write_line("Restart\n")
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
        if str(event.src_path).endswith(".py"):
            self._observer.stop()
            self._restart()

    def _start(self):
        self._build()
        self._start_observer()
        self._ls_thread = LiveServerThread(
            self._project_settings.python_executable, self._wd, self._args, self._env, self._build_settings
        )
        self._ls_thread.start()
        self._ls_thread.join()
        Console.close()

    def _build(self):
        if self._is_dev:
            return

        self._env.set_working_directory(self._src_dir)
        self._publisher.build()
        self._env.set_working_directory(self._src_dir)
        self._wd = os.path.abspath(
            os.path.join(
                self._src_dir,
                self._build_settings.output_path,
                self._project_settings.name,
                "build",
                String.convert_to_snake_case(self._project_settings.name),
            )
        )

    def start(self, args: list[str]):
        """
        Starts the CPL live development server
        :param args:
        :return:
        """
        if self._build_settings.main == "":
            Console.error("Project has no entry point.")
            return

        if "dev" in args:
            self._is_dev = True
            args.remove("dev")

        self._args = args
        Console.write_line("** CPL live development server is running **")
        self._start()
