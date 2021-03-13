from cpl_cli.command_abc import CommandABC
from cpl_cli.live_server.live_server_service import LiveServerService


class StartService(CommandABC):

    def __init__(self, live_server: LiveServerService):
        CommandABC.__init__(self)

        self._live_server = live_server

    def run(self, args: list[str]):
        self._live_server.start()
