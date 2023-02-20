from cpl_core.configuration.argument_abc import ArgumentABC


class FlagArgument(ArgumentABC):
    def __init__(
        self,
        token: str,
        name: str,
        aliases: list[str],
        prevent_next_executable: bool = False,
        console_arguments: list["ArgumentABC"] = None,
    ):
        ArgumentABC.__init__(self, token, name, aliases, prevent_next_executable, console_arguments)
