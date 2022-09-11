import discord

from cpl_core.logging import LoggerABC
from cpl_discord.events.on_ready_abc import OnReadyABC
from cpl_discord.service.discord_bot_service_abc import DiscordBotServiceABC


class OnReadyEvent(OnReadyABC):

    def __init__(self, logger: LoggerABC, bot: DiscordBotServiceABC):
        OnReadyABC.__init__(self)
        self._logger = logger
        self._bot = bot

    def _log(self, _t: str, _o: object, _type: type = None):
        self._logger.debug(__name__, f'{_t} {_o} {_type}')

    async def on_ready(self):
        self._logger.info(__name__, 'Hello World')
        for g in self._bot.guilds:
            self._log('-Guild', g, type(g))
            for r in g.roles:
                self._log('--Role', r, type(r))
                for rm in r.members:
                    self._log('---Rolemembers', rm, type(rm))

            for m in g.members:
                self._log('--Member', m, type(m))

        select = self._bot.guilds.select(lambda guild: (guild.name, guild.id))
        self._logger.warn(__name__, f'Does cpl.query select work? {select}')
        select_many = self._bot.guilds.select_many(lambda guild: guild.roles).where(lambda role: role.name == "Tester").first()
        self._logger.warn(__name__, f'Does cpl.query select_many work? {select_many}')
