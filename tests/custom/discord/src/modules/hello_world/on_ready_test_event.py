from cpl_core.logging import LoggerABC
from cpl_discord.events.on_ready_abc import OnReadyABC


class OnReadyTestEvent(OnReadyABC):
    def __init__(self, logger: LoggerABC):
        OnReadyABC.__init__(self)
        self._logger = logger

    async def on_ready(self):
        self._logger.info(__name__, "Test second on ready")
