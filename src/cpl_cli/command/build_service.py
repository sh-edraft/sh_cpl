from cpl.console.console import Console
from cpl_cli.command_abc import CommandABC
from cpl_cli.publish.publisher_abc import PublisherABC


class BuildService(CommandABC):

    def __init__(self, publisher: PublisherABC):
        CommandABC.__init__(self)

        self._publisher = publisher

    def run(self, args: list[str]):
        self._publisher.build()
        Console.write('\n')
