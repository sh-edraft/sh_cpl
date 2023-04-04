from abc import ABC, abstractmethod


class PipeABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def transform(self, value: any, *args):
        pass
