from abc import abstractmethod, ABC


class LoggerABC(ABC):
    r"""ABC for :class:`cpl_core.logging.logger_service.Logger`"""

    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def header(self, string: str):
        r"""Writes a header message

        Parameter
        ---------
            string: :class:`str`
                String to write as header
        """
        pass

    @abstractmethod
    def trace(self, name: str, message: str):
        r"""Writes a trace message

        Parameter
        ---------
            name: :class:`str`
                Message name
            message: :class:`str`
                Message string
        """
        pass

    @abstractmethod
    def debug(self, name: str, message: str):
        r"""Writes a debug message

        Parameter
        ---------
            name: :class:`str`
                Message name
            message: :class:`str`
                Message string
        """
        pass

    @abstractmethod
    def info(self, name: str, message: str):
        r"""Writes an information

        Parameter
        ---------
            name: :class:`str`
                Message name
            message: :class:`str`
                Message string
        """
        pass

    @abstractmethod
    def warn(self, name: str, message: str):
        r"""Writes an warning

        Parameter
        ---------
            name: :class:`str`
                Message name
            message: :class:`str`
                Message string
        """
        pass

    @abstractmethod
    def error(self, name: str, message: str, ex: Exception = None):
        r"""Writes an error

        Parameter
        ---------
            name: :class:`str`
                Error name
            message: :class:`str`
                Error message
            ex: :class:`Exception`
                Thrown exception
        """
        pass

    @abstractmethod
    def fatal(self, name: str, message: str, ex: Exception = None):
        r"""Writes an error and ends the program

        Parameter
        ---------
            name: :class:`str`
                Error name
            message: :class:`str`
                Error message
            ex: :class:`Exception`
                Thrown exception
        """
        pass
