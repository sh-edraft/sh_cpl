from cpl_cli.migrations.base.migration_abc import MigrationABC
from cpl_cli.migrations.base.migration_service_abc import MigrationServiceABC
from cpl_cli.migrations.migration_2022_10 import Migration202210
from cpl_cli.migrations.service.migration_service import MigrationService
from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC


class StartupMigrationExtension(StartupExtensionABC):
    def __init__(self):
        pass

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        pass

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        services.add_singleton(MigrationServiceABC, MigrationService)
        services.add_singleton(MigrationABC, Migration202210)
