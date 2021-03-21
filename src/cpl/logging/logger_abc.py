from abc import abstractmethod

from cpl.dependency_injection.service_abc import ServiceABC


class LoggerABC(ServiceABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for logging
        """
        ServiceABC.__init__(self)

    @abstractmethod
    def header(self, string: str):
        """
        Writes a header message
        :param string:
        :return:
        """
        pass

    @abstractmethod
    def trace(self, name: str, message: str):
        """
        Writes a trace message
        :param name:
        :param message:
        :return:
        """
        pass

    @abstractmethod
    def debug(self, name: str, message: str):
        """
        Writes a debug message
        :param name:
        :param message:
        :return:
        """
        pass

    @abstractmethod
    def info(self, name: str, message: str):
        """
        Writes an information
        :param name:
        :param message:
        :return:
        """
        pass

    @abstractmethod
    def warn(self, name: str, message: str):
        """
        Writes an warning
        :param name:
        :param message:
        :return:
        """
        pass

    @abstractmethod
    def error(self, name: str, message: str, ex: Exception = None):
        """
        Writes an error
        :param name:
        :param message:
        :param ex:
        :return:
        """
        pass

    @abstractmethod
    def fatal(self, name: str, message: str, ex: Exception = None):
        """
        Writes an error and exits
        :param name:
        :param message:
        :param ex:
        :return:
        """
        pass
