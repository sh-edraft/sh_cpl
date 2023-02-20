import threading

from unittests_shared.cli_commands import CLICommands


class StartTestThread(threading.Thread):
    def __init__(self, is_dev=False):
        threading.Thread.__init__(self, daemon=True)
        self._is_dev = is_dev

    def run(self):
        CLICommands.start(is_dev=self._is_dev, output=True)
