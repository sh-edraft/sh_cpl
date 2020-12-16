from sh_edraft.cli.command.base.command_base import CommandBase
from sh_edraft.configuration.base.configuration_base import ConfigurationBase
from sh_edraft.console.console import Console
from sh_edraft.publishing.publisher import Publisher
from sh_edraft.publishing.base.publisher_base import PublisherBase
from sh_edraft.service.providing.service_provider import ServiceProviderBase


class Build(CommandBase):

    def __init__(self, services: ServiceProviderBase, config: ConfigurationBase):
        CommandBase.__init__(self)
        self._services = services
        self._config = config

        self._aliases.append('-b')
        self._aliases.append('-B')
        self._publisher: Publisher = self._services.get_service(PublisherBase)

    def run(self, args: list[str]):
        if len(args) > 0:
            Console.error(f'Invalid arguments {args}')
            Console.error('Run \'cpl help\'')

        self._publisher.create()
        self._publisher.publish()
