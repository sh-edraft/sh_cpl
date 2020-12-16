import sys
import traceback

from sh_edraft.cli.cpl_cli.commands.build.build import Build
from sh_edraft.cli.cpl_cli.commands.help import Help
from sh_edraft.cli.cpl_cli.commands.new import New
from sh_edraft.cli.cpl_cli.commands.publish.publish import Publish
from sh_edraft.cli.cpl_cli.commands.version import Version
from sh_edraft.cli.interpreter.interpreter import Interpreter
from sh_edraft.console.console import Console


class CLI:

    def __init__(self):
        self._interpreter = Interpreter()

    def setup(self):
        self._interpreter.add_command(Build())
        self._interpreter.add_command(Help())
        self._interpreter.add_command(New())
        self._interpreter.add_command(Publish())
        self._interpreter.add_command(Version())

    def main(self):
        string = ' '.join(sys.argv[1:])
        try:
            self._interpreter.interpret(string)
        except Exception as e:
            tb = traceback.format_exc()
            Console.error(str(e), tb)
            Console.error('Run \'cpl help\'')


def main():
    cli = CLI()
    cli.setup()
    cli.main()


if __name__ == '__main__':
    main()
