from abc import abstractmethod

from cpl.dependency_injection.service_abc import ServiceABC


class LoggerABC(ServiceABC):

    @abstractmethod
    def __init__(self):
        ServiceABC.__init__(self)

    @abstractmethod
    def header(self, string: str): pass

    @abstractmethod
    def trace(self, name: str, message: str): pass

    @abstractmethod
    def debug(self, name: str, message: str): pass

    @abstractmethod
    def info(self, name: str, message: str): pass

    @abstractmethod
    def warn(self, name: str, message: str): pass

    @abstractmethod
    def error(self, name: str, message: str, ex: Exception = None): pass

    @abstractmethod
    def fatal(self, name: str, message: str, ex: Exception = None): pass
