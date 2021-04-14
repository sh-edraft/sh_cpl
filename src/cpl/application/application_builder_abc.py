from abc import ABC, abstractmethod
from typing import Type

from cpl.application.application_abc import ApplicationABC
from cpl.application.startup_abc import StartupABC


class ApplicationBuilderABC(ABC):
    r"""ABC for the :class:`cpl.application.application_builder.ApplicationBuilder`"""

    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def use_startup(self, startup: Type[StartupABC]):
        r"""Sets the custom startup class to use

        Parameter
        ---------
            startup: Type[:class:`cpl.application.startup_abc.StartupABC`]
                Type of :class:`cpl.application.startup_abc.StartupABC`
        """
        pass

    @abstractmethod
    def build(self) -> ApplicationABC:
        r"""Creates custom application object

        Returns
        -------
            Object of :class:`cpl.application.application_abc.ApplicationABC`
        """
        pass
