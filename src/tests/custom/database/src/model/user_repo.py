from cpl_core.database.context import DatabaseContextABC
from .city_model import CityModel
from .user_model import UserModel
from .user_repo_abc import UserRepoABC


class UserRepo(UserRepoABC):

    def __init__(self, db_context: DatabaseContextABC):
        UserRepoABC.__init__(self)

        self._db: DatabaseContextABC = db_context

    def create(self): pass

    def add_test_user(self):
        city = CityModel('Haren', '49733')
        city2 = CityModel('Meppen', '49716')
        self._db.cursor.execute(city2.insert_string)
        user = UserModel('TestUser', city)
        self._db.cursor.execute(user.insert_string)

    def get_users(self) -> list[UserModel]:
        self._db.cursor.execute(f"""SELECT * FROM `User`""")
        return self._db.cursor.fetchall()

    def get_cities(self) -> list[CityModel]:
        self._db.cursor.execute(f"""SELECT * FROM `City`""")
        return self._db.cursor.fetchall()
