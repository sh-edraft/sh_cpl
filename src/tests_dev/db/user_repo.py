from sh_edraft.database.context.base import DatabaseContextBase
from tests_dev.db.city import City
from tests_dev.db.user import User
from tests_dev.db.user_repo_base import UserRepoBase


class UserRepo(UserRepoBase):

    def __init__(self, db_context: DatabaseContextBase):
        UserRepoBase.__init__(self)

        self._session = db_context.session
        self._user_query = db_context.session.query(User)

    def create(self): pass

    def add_test_user(self):
        city = City('Haren', '49733')
        city2 = City('Meppen', '49716')
        self._session.add(city2)
        user = User('TestUser', city)
        self._session.add(user)
        self._session.commit()
