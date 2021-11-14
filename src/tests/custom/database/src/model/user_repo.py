from cpl_core.database.context import DatabaseContextABC
from .city_model import CityModel
from .user_model import UserModel
from .user_repo_abc import UserRepoABC


class UserRepo(UserRepoABC):

    def __init__(self, db_context: DatabaseContextABC):
        UserRepoABC.__init__(self)

        self._session = db_context.session
        self._user_query = db_context.session.query(UserModel)

    def create(self): pass

    def add_test_user(self):
        city = CityModel('Haren', '49733')
        city2 = CityModel('Meppen', '49716')
        self._session.add(city2)
        user = UserModel('TestUser', city)
        self._session.add(user)
        self._session.commit()

    def get_users(self) -> list[UserModel]:
        return self._session.query(UserModel).all()

    def get_cities(self) -> list[CityModel]:
        return self._session.query(CityModel).all()
