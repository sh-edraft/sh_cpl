from abc import ABC, abstractmethod

from .user_model import UserModel


class UserRepoABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def get_users(self) -> list[UserModel]: pass
