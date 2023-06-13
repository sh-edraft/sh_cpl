from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class DatabaseSettings(ConfigurationModelABC):
    r"""Represents settings for the database connection"""

    def __init__(
        self,
        host: str = None,
        port: int = 3306,
        user: str = None,
        password: str = None,
        database: str = None,
        charset: str = None,
        use_unicode: bool = None,
        buffered: bool = None,
        auth_plugin: str = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._host: Optional[str] = host
        self._port: Optional[int] = port
        self._user: Optional[str] = user
        self._password: Optional[str] = password
        self._databse: Optional[str] = database
        self._charset: Optional[str] = charset
        self._use_unicode: Optional[bool] = use_unicode
        self._buffered: Optional[bool] = buffered
        self._auth_plugin: Optional[str] = auth_plugin

    @property
    def host(self) -> Optional[str]:
        return self._host

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def user(self) -> Optional[str]:
        return self._user

    @property
    def password(self) -> Optional[str]:
        return self._password

    @property
    def database(self) -> Optional[str]:
        return self._databse

    @property
    def charset(self) -> Optional[str]:
        return self._charset

    @property
    def use_unicode(self) -> Optional[bool]:
        return self._use_unicode

    @property
    def buffered(self) -> Optional[bool]:
        return self._buffered

    @property
    def auth_plugin(self) -> Optional[str]:
        return self._auth_plugin
