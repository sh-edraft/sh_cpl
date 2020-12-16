import sys
import traceback
from typing import Optional

from sh_edraft.cli.cpl_cli.commands.build import Build
from sh_edraft.cli.cpl_cli.commands.help import Help
from sh_edraft.cli.cpl_cli.commands.new import New
from sh_edraft.cli.cpl_cli.commands.version import Version
from sh_edraft.cli.interpreter.interpreter import Interpreter
from sh_edraft.configuration.base import ConfigurationBase
from sh_edraft.console.console import Console
from sh_edraft.hosting.application_host import ApplicationHost
from sh_edraft.hosting.base.application_base import ApplicationBase
from sh_edraft.logging.logger import Logger
from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publishing.publisher import Publisher
from sh_edraft.publishing.base.publisher_base import PublisherBase
from sh_edraft.service.providing.service_provider import ServiceProviderBase


class CLI(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None
        self._services: Optional[ServiceProviderBase] = None
        self._configuration: Optional[ConfigurationBase] = None
        self._logger: Optional[LoggerBase] = None

        self._interpreter = Interpreter()

    def create_application_host(self):
        self._app_host = ApplicationHost()
        self._configuration = self._app_host.configuration
        self._services = self._app_host.services

    def create_configuration(self):
        self._configuration.add_json_file(f'project.json')

    def create_services(self):
        self._services.add_singleton(LoggerBase, Logger)
        self._logger = self._services.get_service(LoggerBase)
        self._services.add_singleton(PublisherBase, Publisher)

    def setup(self):
        self._interpreter.add_command(Build(self._services, self._configuration))
        self._interpreter.add_command(Help())
        self._interpreter.add_command(New())
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
    cli.create_application_host()
    cli.create_configuration()
    cli.create_services()
    cli.setup()
    cli.main()


if __name__ == '__main__':
    main()
