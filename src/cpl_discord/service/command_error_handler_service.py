from discord.ext.commands import Context, CommandError

from cpl_core.logging import LoggerABC
from cpl_discord.events.on_command_error_abc import OnCommandErrorABC


class CommandErrorHandlerService(OnCommandErrorABC):

    def __init__(self, logger: LoggerABC):
        OnCommandErrorABC.__init__(self)
        self._logger = logger

    async def on_command_error(self, ctx: Context, error: CommandError):
        self._logger.error(__name__, f'Error in command: {ctx.command}', error)
