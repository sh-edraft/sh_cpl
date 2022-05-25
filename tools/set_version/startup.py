import os

from cpl_cli.configuration import WorkspaceSettings
from cpl_core.application import StartupABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironment
from cpl_core.pipes.version_pipe import VersionPipe
from set_version.git_service import GitService
from set_version.version_setter_service import VersionSetterService


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
        configuration.add_json_file('cpl-workspace.json', optional=True, output=False)
        if configuration.get_configuration(WorkspaceSettings) is None:
            environment.set_working_directory(os.path.join(environment.working_directory, '../../'))
            configuration.add_json_file('cpl-workspace.json', optional=False, output=False)

        return configuration

    def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
        services.add_transient(GitService)
        services.add_transient(VersionSetterService)
        services.add_transient(VersionPipe)

        return services.build_service_provider()
