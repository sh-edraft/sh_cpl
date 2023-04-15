from abc import ABC, abstractmethod


class Unsubscribable(ABC):
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def unsubscribe(self):
        pass
