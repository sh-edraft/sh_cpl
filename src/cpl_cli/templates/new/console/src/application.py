from cpl.application.application_abc import ApplicationABC
from cpl.console.console import Console


class Application(ApplicationABC):

    def __init__(self):
        ApplicationABC.__init__(self)

    def configure(self):
        pass

    def main(self):
        Console.write_line('Hello World')
