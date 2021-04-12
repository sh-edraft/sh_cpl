import textwrap

from cpl_cli.command_abc import CommandABC
from cpl_cli.live_server.live_server_service import LiveServerService


class StartService(CommandABC):

    def __init__(self, live_server: LiveServerService):
        """
        Service for the CLI command start
        :param live_server:
        """
        CommandABC.__init__(self)

        self._live_server = live_server

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Starts your application, restarting on file changes.
        Usage: cpl start
        """)

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        self._live_server.start(args)
