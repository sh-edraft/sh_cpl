from cpl.console.console import Console
from cpl.dependency_injection.service_abc import ServiceABC


class Help(ServiceABC):

    def __init__(self):
        ServiceABC.__init__(self)

    def run(self, args: list[str]):
        Console.write_line('Available Commands:')
        commands = [
            ['build (-b|-B)', 'Prepares files for publishing into an output directory named dist/ at the given output path. Must be executed from within a workspace directory.'],
            ['help (-h|-H)', 'Lists available commands and their short descriptions.'],
            ['new', 'Creates a new file or package.'],
            ['publish (-p|-P)', 'Prepares files for publishing into an output directory named dist/ at the given output path and executes setup.py. Must be executed from within a workspace directory.'],
            ['version (-v|-V)', 'Outputs CPL CLI version.']
        ]
        for name, description in commands:
            Console.set_foreground_color('blue')
            Console.write(f'\n\t{name} ')
            Console.set_foreground_color('default')
            Console.write(f'{description}')

        Console.write('\n')
