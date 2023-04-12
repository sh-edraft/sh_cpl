from abc import ABC, abstractmethod


class OnDisconnectABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_disconnect(self):
        pass
