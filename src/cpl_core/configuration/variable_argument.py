from cpl_core.configuration.argument_abc import ArgumentABC


class VariableArgument(ArgumentABC):

    def __init__(self,
                 token: str,
                 name: str,
                 aliases: list[str],
                 value_token: str,
                 prevent_next_executable: bool = False,
                 console_arguments: list['ArgumentABC'] = None
                 ):
        self._value_token = value_token
        self._value: str = ''

        ArgumentABC.__init__(self, token, name, aliases, prevent_next_executable, console_arguments)

    @property
    def value_token(self) -> str:
        return self._value_token

    @property
    def value(self) -> str:
        return self._value

    def set_value(self, value: str):
        self._value = value
