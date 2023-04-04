from discord.ext import commands
from discord.ext.commands import Context

from cpl_core.logging import LoggerABC
from cpl_discord.command.discord_command_abc import DiscordCommandABC
from cpl_discord.service.discord_bot_service_abc import DiscordBotServiceABC


class PingCommand(DiscordCommandABC):
    def __init__(
        self,
        logger: LoggerABC,
        bot: DiscordBotServiceABC,
    ):
        DiscordCommandABC.__init__(self)

        self._logger = logger
        self._bot = bot

        self._logger.trace(__name__, f"Loaded command service: {type(self).__name__}")

    @commands.hybrid_command()
    async def ping(self, ctx: Context):
        self._logger.debug(__name__, f"Received command ping {ctx}")
        self._logger.info(__name__, f"Bot name {self._bot.user.name}")
        self._logger.trace(__name__, f"Finished ping command")
        await ctx.send("Pong")
