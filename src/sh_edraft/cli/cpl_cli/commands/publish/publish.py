from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.cli.cpl_cli.commands.publish.app import PublishApp
from sh_edraft.console.console import Console


class Publish(CommandBase):

    def __init__(self):
        CommandBase.__init__(self)
        self._app = PublishApp()

        self._aliases.append('-b')
        self._aliases.append('-B')

    def run(self, args: list[str]):
        if len(args) > 0:
            Console.error(f'Invalid arguments {args}')
            Console.error('Run \'cpl help\'')

        self._app.create_application_host()
        self._app.create_configuration()
        self._app.create_services()
        self._app.main()
