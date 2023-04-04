from abc import ABC, abstractmethod


class OnReadyABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_ready(self):
        pass
