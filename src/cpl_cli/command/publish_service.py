import textwrap

from cpl_cli.command_abc import CommandABC
from cpl_cli.publish.publisher_abc import PublisherABC


class PublishService(CommandABC):

    def __init__(self, publisher: PublisherABC):
        """
        Service for the CLI command publish
        :param publisher:
        """
        CommandABC.__init__(self)

        self._publisher = publisher

    @property
    def help_message(self) -> str:
        return textwrap.dedent("""\
        Prepares files for publish into an output directory named dist/ at the given output path and executes setup.py.
        Usage: cpl publish
        """)

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        self._publisher.publish()
