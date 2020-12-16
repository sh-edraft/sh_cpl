from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.console.console import Console


class Help(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)

    def run(self, args: list[str]):
        Console.write_line('Available Commands:')
