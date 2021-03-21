from abc import ABC, abstractmethod


class ServiceABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC to represent a service
        """
        pass
