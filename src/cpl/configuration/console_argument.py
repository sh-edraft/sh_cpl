class ConsoleArgument:

    def __init__(self, token: str, name: str, aliases: list[str], value_token: str):
        self._token = token
        self._name = name
        self._aliases = aliases
        self._value_token = value_token

    @property
    def token(self):
        return self._token

    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
    
    @property
    def value_token(self):
        return self._value_token
