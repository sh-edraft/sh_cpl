from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class CLISettings(ConfigurationModelABC):
    def __init__(self, pip_path: str = None):
        ConfigurationModelABC.__init__(self)

        self._pip_path: Optional[str] = pip_path

    @property
    def pip_path(self) -> str:
        return self._pip_path
