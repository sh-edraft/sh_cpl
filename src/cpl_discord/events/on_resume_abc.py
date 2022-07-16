from abc import ABC, abstractmethod


class OnResumeABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_resume(self): pass