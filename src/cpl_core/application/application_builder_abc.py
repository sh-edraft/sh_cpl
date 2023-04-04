from abc import ABC, abstractmethod
from typing import Type

from cpl_core.application.application_abc import ApplicationABC
from cpl_core.application.startup_abc import StartupABC


class ApplicationBuilderABC(ABC):
    r"""ABC for the :class:`cpl_core.application.application_builder.ApplicationBuilder`"""

    @abstractmethod
    def __init__(self, *args):
        pass

    @abstractmethod
    def use_startup(self, startup: Type[StartupABC]):
        r"""Sets the custom startup class to use

        Parameter:
            startup: Type[:class:`cpl_core.application.startup_abc.StartupABC`]
                Startup class to use
        """
        pass

    @abstractmethod
    async def use_startup(self, startup: Type[StartupABC]):
        r"""Sets the custom startup class to use async

        Parameter:
            startup: Type[:class:`cpl_core.application.startup_abc.StartupABC`]
                Startup class to use
        """
        pass

    @abstractmethod
    def build(self) -> ApplicationABC:
        r"""Creates custom application object

        Returns:
            Object of :class:`cpl_core.application.application_abc.ApplicationABC`
        """
        pass

    @abstractmethod
    async def build_async(self) -> ApplicationABC:
        r"""Creates custom application object async

        Returns:
            Object of :class:`cpl_core.application.application_abc.ApplicationABC`
        """
        pass
