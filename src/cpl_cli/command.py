from cpl.dependency_injection.service_abc import ServiceABC


class Command:

    def __init__(self, name: str, aliases: list[str], command: ServiceABC):
        self._name = name
        self._aliases = aliases
        self._command = command

    @property
    def name(self):
        return self._name

    @property
    def aliases(self):
        return self._aliases
    
    @property
    def command(self):
        return self._command
