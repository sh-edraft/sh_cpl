class ConsoleArgument:

    def __init__(self,
                 token: str,
                 name: str,
                 aliases: list[str],
                 value_token: str,
                 is_value_token_optional: bool = None,
                 console_arguments: list['ConsoleArgument'] = None
                 ):
        """
        Representation of an console argument
        :param token:
        :param name:
        :param aliases:
        :param value_token:
        :param is_value_token_optional:
        :param console_arguments:
        """
        self._token = token
        self._name = name
        self._aliases = aliases
        self._value_token = value_token
        self._is_value_token_optional = is_value_token_optional
        self._console_arguments = console_arguments

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
    def is_value_token_optional(self) -> bool:
        return self._is_value_token_optional

    @property
    def console_arguments(self) -> list['ConsoleArgument']:
        return self._console_arguments
