import textwrap

from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Command(GenerateSchematicABC):
    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        code = """\
        from cpl_core.logging import LoggerABC
        from cpl_discord.command import DiscordCommandABC
        from cpl_discord.service import DiscordBotServiceABC
        from discord.ext import commands
        from discord.ext.commands import Context
        
        
        class $Name(DiscordCommandABC):
        
            def __init__(
                    self,
                    logger: LoggerABC,
                    bot: DiscordBotServiceABC
            ):
                DiscordCommandABC.__init__(self)
        
                self._logger = logger
                self._bot = bot
        
            @commands.hybrid_command()
            async def ping(self, ctx: Context):
                await ctx.send('Pong')
        """
        return self.build_code_str(code, Name=self._class_name)

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(cls, "command", [])
