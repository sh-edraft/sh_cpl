import threading

from unittests_shared.cli_commands import CLICommands


class StartTestThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        CLICommands.start()
