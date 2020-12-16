import sys

from sh_edraft.cli.cpl_cli.commands.help import Help
from sh_edraft.cli.cpl_cli.commands.new import New
from sh_edraft.cli.interpreter.interpreter import Interpreter


class CLI:

    def __init__(self):
        self._interpreter = Interpreter()

    def setup(self):
        self._interpreter.add_command(New())
        self._interpreter.add_command(Help())

    def main(self):
        print('CPL CLI:')
        string = ' '.join(sys.argv[1:])
        try:
            self._interpreter.interpret(string)
        except Exception as e:
            print(e)


def main():
    cli = CLI()
    cli.setup()
    cli.main()


if __name__ == '__main__':
    main()
