from abc import ABC, abstractmethod


class OnErrorABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_error(self, event: str, *args, **kwargs): pass