from sh_edraft.cli.command.base.command_base import CommandBase


class Help(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)

    def run(self, args: list[str]):
        print('Commands:')
