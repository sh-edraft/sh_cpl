from cpl_cli.migrations.base.migration_abc import MigrationABC


class Migration202210(MigrationABC):

    def __init__(self):
        MigrationABC.__init__(self, '2022.10')

    def migrate(self):
        # This migration could be deleted, but stays as an example.
        pass
