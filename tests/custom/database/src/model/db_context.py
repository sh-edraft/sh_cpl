from cpl_core.database import DatabaseSettings
from cpl_core.database.context import DatabaseContext


class DBContext(DatabaseContext):
    def __init__(self):
        DatabaseContext.__init__(self)
