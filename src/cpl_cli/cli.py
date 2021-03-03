from cpl.application.application_abc import ApplicationABC
from cpl.console.console import Console


class CLI(ApplicationABC):

    def __init__(self):
        ApplicationABC.__init__(self)

    def configure(self):
        if self._services is None:
            Console.error('Service provider is empty')
            exit()

        if self._configuration is None:
            Console.error('Configuration is empty')
            exit()

    def main(self):
        Console.write_line(self._configuration)
