from abc import ABC, abstractmethod


class ValidatorABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass
