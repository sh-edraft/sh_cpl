from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class TestStartup_extension(StartupExtensionABC):

    def __init__(self):
        pass

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        pass

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        pass
