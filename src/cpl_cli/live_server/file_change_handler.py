from watchdog.events import FileSystemEventHandler

from cpl.console.console import Console
from cpl_cli.live_server.live_server import LiveServerThread


class FileChangeHandler(FileSystemEventHandler):

    def __init__(self, live_server: LiveServerThread):
        FileSystemEventHandler.__init__(self)

        self._live_server = live_server

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            if str(event.src_path).endswith('.py'):
                Console.write_line(f'Detected change in {event.src_path}')
                self._live_server.kill_application()
                self._live_server.start()
