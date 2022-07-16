from abc import abstractmethod

from cpl_core.application import ApplicationABC


class DiscordBotApplicationABC(ApplicationABC):

    def __init__(self):
        pass

    @abstractmethod
    def stop_async(self): pass
