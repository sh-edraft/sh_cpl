from sh_edraft.cli.command.base.command_base import CommandBase


class Interpreter:

    def __init__(self):
        self._commands: list[CommandBase] = []

    def add_command(self, command: CommandBase):
        self._commands.append(command)

    def remove_command(self, command: CommandBase):
        self._commands.remove(command)

    def interpret(self, input_string: str):
        input_list = input_string.split(' ')
        commands = [type(cmd).__name__.lower() for cmd in self._commands]
        command = input_list[0]
        args = input_list[1:]
        print(command)
        if command in commands:
            cmd = next((cmd for cmd in self._commands if type(cmd).__name__.lower() == command), None)
            if cmd is not None:
                cmd.run(args)
            else:
                print(f'Unexpected command {command}')
        else:
            print(f'Unexpected command {command}')
