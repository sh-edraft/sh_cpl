from cpl_core.console import Console
from cpl_core.database.context import DatabaseContextABC

from .city_model import CityModel
from .user_model import UserModel
from .user_repo_abc import UserRepoABC


class UserRepo(UserRepoABC):
    def __init__(self, db_context: DatabaseContextABC):
        UserRepoABC.__init__(self)

        self._db_context: DatabaseContextABC = db_context

    def add_test_user(self):
        city = CityModel("Haren", "49733")
        city2 = CityModel("Meppen", "49716")
        self._db_context.cursor.execute(city2.insert_string)
        user = UserModel("TestUser", city)
        self._db_context.cursor.execute(user.insert_string)
        self._db_context.save_changes()

    def get_users(self) -> list[UserModel]:
        users = []
        results = self._db_context.select("SELECT * FROM `User`")
        for result in results:
            users.append(UserModel(result[1], self.get_city_by_id(result[2]), id=result[0]))
        return users

    def get_cities(self) -> list[CityModel]:
        cities = []
        results = self._db_context.select("SELECT * FROM `City`")
        for result in results:
            cities.append(CityModel(result[1], result[2], id=result[0]))
        return cities

    def get_city_by_id(self, id: int) -> CityModel:
        if id is None:
            return None
        result = self._db_context.select(f"SELECT * FROM `City` WHERE `Id` = {id}")
        return CityModel(result[1], result[2], id=result[0])
