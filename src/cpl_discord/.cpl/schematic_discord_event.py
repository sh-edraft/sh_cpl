import sys
import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC
from cpl_core.console import Console
from cpl_core.utils import String


class Event(GenerateSchematicABC):
    def __init__(self, name: str, schematic: str, path: str):
        GenerateSchematicABC.__init__(self, name, schematic, path)

        event = None

        from cpl_discord.discord_event_types_enum import DiscordEventTypesEnum

        for event_type in DiscordEventTypesEnum:
            event_name = event_type.value.__name__.replace("ABC", "")

            if event_name in name:
                name = name.replace(event_name, "")
                event = event_name
                break

        if event is None:
            Console.error(f"No valid event found in name {name}")
            Console.write_line("Available events:")
            for event_type in DiscordEventTypesEnum:
                Console.write_line(f'\t{event_type.value.__name__.replace("ABC", "")}')
            sys.exit()

        self._event_class = f"{event}ABC"
        self._name = f'{String.convert_to_snake_case(self._event_class.replace("ABC", ""))}_{schematic}.py'
        self._class_name = f'{self._event_class.replace("ABC", "")}{String.first_to_upper(schematic)}'
        if name != "":
            self._name = f"{String.convert_to_snake_case(name)}_{self._name}"
            self._class_name = f"{String.first_to_upper(name)}{self._class_name}"

    def get_code(self) -> str:
        code = """\
        from cpl_core.logging import LoggerABC
        from cpl_discord.events import $EventClass
        from cpl_discord.service import DiscordBotServiceABC
        
        
        class $Name($EventClass):
        
            def __init__(
                    self,
                    logger: LoggerABC,
                    bot: DiscordBotServiceABC,
            ):
                OnReadyABC.__init__(self)
        
                self._logger = logger
                self._bot = bot
        
            async def on_ready(self):
                pass
        """
        return self.build_code_str(code, Name=self._class_name, EventClass=self._event_class)

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "event", [])
