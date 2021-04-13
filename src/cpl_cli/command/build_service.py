import textwrap

from cpl_cli.command_abc import CommandABC
from cpl_cli.publish.publisher_abc import PublisherABC


class BuildService(CommandABC):

    def __init__(self, publisher: PublisherABC):
        """
        Service for the CLI command build
        :param publisher:
        """
        CommandABC.__init__(self)

        self._publisher = publisher

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Copies an python app into an output directory named build/ at the given output path. Must be executed within a CPL workspace or project directory
        Usage: cpl build
        """)

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        self._publisher.build()
