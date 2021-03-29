from abc import abstractmethod, ABC


class LoggerABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC for logging
        """
        ABC.__init__(self)

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
