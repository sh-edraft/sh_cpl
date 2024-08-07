from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class EMailClientSettings(ConfigurationModelABC):
    r"""Representation of mailing settings"""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        user_name: str = None,
        credentials: str = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._host: str = host
        self._port: int = port
        self._user_name: str = user_name
        self._credentials: str = credentials

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, host: str) -> None:
        self._host = host

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, port: int) -> None:
        self._port = port

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, user_name: str) -> None:
        self._user_name = user_name

    @property
    def credentials(self) -> str:
        return self._credentials

    @credentials.setter
    def credentials(self, credentials: str) -> None:
        self._credentials = credentials
