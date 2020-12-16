from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.console.console import Console


class Help(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)
        self._aliases.append('-h')
        self._aliases.append('-H')

    def run(self, args: list[str]):
        Console.write_line('Available Commands:')
        commands = [
            ['build (-b|-B)', 'Prepares files for publishing into an output directory named dist/ at the given output path.Must be executed from within a workspace directory.'],
            ['help (-h|-H)', 'Lists available commands and their short descriptions.'],
            ['new', 'Creates a new file or package.'],
            ['version (-v|-V)', 'Outputs CPL CLI version.']
        ]
        for name, description in commands:
            Console.set_foreground_color('blue')
            Console.write(f'\n\t{name} ')
            Console.set_foreground_color('default')
            Console.write(f'{description}')
