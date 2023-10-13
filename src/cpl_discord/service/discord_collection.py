from typing import Type

from cpl_core.console import Console, ForegroundColorEnum
from cpl_core.dependency_injection import ServiceCollectionABC
from cpl_discord.command.discord_command_abc import DiscordCommandABC
from cpl_discord.discord_event_types_enum import DiscordEventTypesEnum
from cpl_discord.service.command_error_handler_service import CommandErrorHandlerService
from cpl_discord.service.discord_collection_abc import DiscordCollectionABC


class DiscordCollection(DiscordCollectionABC):
    def __init__(self, service_collection: ServiceCollectionABC):
        DiscordCollectionABC.__init__(self)

        self._services = service_collection

        self._services.add_transient(DiscordEventTypesEnum.on_command_error.value, CommandErrorHandlerService)

    def add_command(self, _t: Type[DiscordCommandABC]):
        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.write_line(
            f"{type(self).__name__}.add_command is deprecated. Instead, use ServiceCollection.add_transient directly!"
        )
        Console.color_reset()
        self._services.add_transient(DiscordCommandABC, _t)

    def add_event(self, _t_event: Type, _t: Type):
        Console.set_foreground_color(ForegroundColorEnum.yellow)
        Console.write_line(
            f"{type(self).__name__}.add_event is deprecated. Instead, use ServiceCollection.add_transient directly!"
        )
        Console.color_reset()
        self._services.add_transient(_t_event, _t)
