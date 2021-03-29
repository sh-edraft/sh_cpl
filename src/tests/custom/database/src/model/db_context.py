from cpl.database import DatabaseSettings
from cpl.database.context import DatabaseContext


class DBContext(DatabaseContext):

    def __init__(self, db_settings: DatabaseSettings):
        DatabaseContext.__init__(self, db_settings)
