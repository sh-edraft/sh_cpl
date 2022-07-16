from typing import Type, Optional

from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceCollectionABC
from cpl_discord.discord_event_types_enum import DiscordEventTypesEnum
from cpl_discord.service.command_error_handler_service import CommandErrorHandlerService
from cpl_discord.service.discord_collection_abc import DiscordCollectionABC
from cpl_query.extension import List

from cpl_cli import CommandABC


class DiscordCollection(DiscordCollectionABC):

    def __init__(self, service_collection: ServiceCollectionABC):
        DiscordCollectionABC.__init__(self)

        self._services = service_collection
        self._events: dict[str, List] = {}
        self._commands = List(type(CommandABC))

        self.add_event(DiscordEventTypesEnum.on_command_error.value, CommandErrorHandlerService)

    def add_command(self, _t: Type[CommandABC]):
        self._services.add_transient(CommandABC, _t)
        self._commands.append(_t)

    def get_commands(self) -> List[CommandABC]:
        return self._commands

    def add_event(self, _t_event: Type, _t: Type):
        self._services.add_transient(_t_event, _t)
        if _t_event not in self._events:
            self._events[_t_event] = List(type(_t_event))

        self._events[_t_event].append(_t)

    def get_events_by_base(self, _t_event: Type) -> Optional[List]:
        if _t_event not in self._events:
            return None
        return self._events[_t_event]
