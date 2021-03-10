from cpl.console.console import Console
from cpl_cli.command_abc import CommandABC


class Help(CommandABC):

    def __init__(self):
        CommandABC.__init__(self)

    def run(self, args: list[str]):
        Console.write_line('Available Commands:')
        commands = [
            ['build (b|B)', 'Prepares files for publish into an output directory named dist/ at the given output path. Must be executed from within a workspace directory.'],
            ['generate (g|G)', 'Generate a new file.'],
            ['help (h|H)', 'Lists available command and their short descriptions.'],
            ['new (n|N)', 'Creates new CPL project.'],
            ['start (s|S)', 'Starts CPL project, restarting on file changes'],
            ['publish (p|P)', 'Prepares files for publish into an output directory named dist/ at the given output path and executes setup_template.py. Must be executed from within a workspace directory.'],
            ['update (u|u)', 'Update CPL and project dependencies.'],
            ['version (v|V)', 'Outputs CPL CLI version.']
        ]
        for name, description in commands:
            Console.set_foreground_color('blue')
            Console.write(f'\n\t{name} ')
            Console.set_foreground_color('default')
            Console.write(f'{description}')

        Console.write('\n')
