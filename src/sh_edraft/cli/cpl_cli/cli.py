import sys

from sh_edraft.cli.cpl_cli.cli_commands import CLICommands


class CLI:

    def __init__(self):
        self._commands: dict = {}

    def setup(self):
        self._commands[CLICommands.new.__name__] = CLICommands.new
        self._commands[CLICommands.help.__name__] = CLICommands.help

    def main(self):
        args = sys.argv[1:]

        try:
            cmd = self._commands[args[0]]
            cmd(args[1:])
        except KeyError:
            CLICommands.unexpected_command(args[0])
        except Exception as e:
            print(e)


def main():
    cli = CLI()
    cli.setup()
    cli.main()


if __name__ == '__main__':
    main()
