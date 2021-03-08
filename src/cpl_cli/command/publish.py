from cpl_cli.command_abc import CommandABC
from cpl_cli.publish.publisher_abc import PublisherABC


class Publish(CommandABC):

    def __init__(self, publisher: PublisherABC):
        CommandABC.__init__(self)

        self._publisher = publisher

    def run(self, args: list[str]):
        self._publisher.publish()
