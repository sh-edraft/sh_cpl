from abc import ABC, abstractmethod


class OnConnectABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_connect(self): pass
