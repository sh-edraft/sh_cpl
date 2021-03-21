from abc import abstractmethod

from cpl.dependency_injection.service_abc import ServiceABC


class CommandABC(ServiceABC):

    @abstractmethod
    def __init__(self):
        ServiceABC.__init__(self)

    @abstractmethod
    def run(self, args: list[str]): pass
