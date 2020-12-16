from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.console.console import Console


class Interpreter:

    def __init__(self):
        self._commands: list[CommandBase] = []

    def add_command(self, command: CommandBase):
        self._commands.append(command)

    def remove_command(self, command: CommandBase):
        self._commands.remove(command)

    def interpret(self, input_string: str):
        input_list = input_string.split(' ')
        command = input_list[0]
        args = input_list[1:] if len(input_list) > 1 else []

        cmd = next(
            (cmd for cmd in self._commands if type(cmd).__name__.lower() == command or command in cmd.aliases),
            None)
        if cmd is not None:
            cmd.run(args)
        else:
            Console.error(f'Unexpected command {command}')
            Console.error('Run \'cpl help\'')
