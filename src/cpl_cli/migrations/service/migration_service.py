from packaging import version

from cpl_cli.migrations.base.migration_abc import MigrationABC
from cpl_cli.migrations.base.migration_service_abc import MigrationServiceABC
from cpl_core.dependency_injection import ServiceProviderABC


class MigrationService(MigrationServiceABC):

    def __init__(self, services: ServiceProviderABC):
        MigrationServiceABC.__init__(self)

        self._services = services

    def migrate_from(self, _v: str):
        for migration_type in MigrationABC.__subclasses__():
            migration: MigrationABC = self._services.get_service(migration_type)
            if version.parse(migration.version) <= version.parse(_v):
                continue

            migration.migrate()
