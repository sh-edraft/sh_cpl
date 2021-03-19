from abc import ABC, abstractmethod
from typing import Type

from cpl.application.application_abc import ApplicationABC
from cpl.application.startup_abc import StartupABC


class ApplicationBuilderABC(ABC):

    def __init__(self, *args):
        """
        ABC of application builder
        """

    @abstractmethod
    def use_startup(self, startup: Type[StartupABC]):
        """
        Sets the used startup class
        :param startup:
        :return:
        """
        pass

    @abstractmethod
    def build(self) -> ApplicationABC:
        """
        Creates application host and runtime
        :return:
        """
        pass
