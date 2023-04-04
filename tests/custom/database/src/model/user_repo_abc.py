from abc import ABC, abstractmethod

from .city_model import CityModel
from .user_model import UserModel


class UserRepoABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_users(self) -> list[UserModel]:
        pass

    @abstractmethod
    def get_cities(self) -> list[CityModel]:
        pass

    @abstractmethod
    def get_city_by_id(self, id: int) -> CityModel:
        pass
