from cpl_core.configuration.argument_abc import ArgumentABC


class FlagArgument(ArgumentABC):

    def __init__(self,
                 token: str,
                 name: str,
                 aliases: list[str],
                 console_arguments: list['ArgumentABC'] = None
                 ):

        ArgumentABC.__init__(self, token, name, aliases, console_arguments)
