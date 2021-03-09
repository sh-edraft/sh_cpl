class ConsoleArgument:

    def __init__(self, token: str, name: str, aliases: list[str], value_token: str, arg_types: list['ConsoleArgument'] = None):
        self._token = token
        self._name = name
        self._aliases = aliases
        self._value_token = value_token
        self._arg_types = arg_types

    @property
    def token(self) -> str:
        return self._token

    @property
    def name(self) -> str:
        return self._name

    @property
    def aliases(self) -> list[str]:
        return self._aliases
    
    @property
    def value_token(self) -> str:
        return self._value_token

    @property
    def arg_types(self) -> list['ConsoleArgument']:
        return self._arg_types
