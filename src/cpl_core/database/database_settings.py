from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class DatabaseSettings(ConfigurationModelABC):
    r"""Represents settings for the database connection"""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        databse: str = None,
        charset: str = None,
        use_unicode: bool = None,
        buffered: bool = None,
        auth_plugin: bool = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._host: Optional[str] = host
        self._port: Optional[int] = port
        self._user: Optional[str] = user
        self._password: Optional[str] = password
        self._databse: Optional[str] = databse
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

    # def from_dict(self, settings: dict):
    #     r"""Sets attributes from given dict
    #
    #     Parameter:
    #     settings: :class:`dict`
    #     """
    #     try:
    #         self._host = settings[DatabaseSettingsNameEnum.host.value]
    #         if DatabaseSettingsNameEnum.port.value in settings:
    #             self._port = settings[DatabaseSettingsNameEnum.port.value]
    #         else:
    #             self._port = 3306
    #         self._user = settings[DatabaseSettingsNameEnum.user.value]
    #         self._password = settings[DatabaseSettingsNameEnum.password.value]
    #         self._databse = settings[DatabaseSettingsNameEnum.database.value]
    #
    #         if DatabaseSettingsNameEnum.charset.value in settings:
    #             self._charset = settings[DatabaseSettingsNameEnum.charset.value]
    #
    #         if DatabaseSettingsNameEnum.buffered.value in settings:
    #             self._use_unicode = bool(settings[DatabaseSettingsNameEnum.use_unicode.value])
    #
    #         if DatabaseSettingsNameEnum.buffered.value in settings:
    #             self._buffered = bool(settings[DatabaseSettingsNameEnum.buffered.value])
    #
    #         if DatabaseSettingsNameEnum.auth_plugin.value in settings:
    #             self._auth_plugin = settings[DatabaseSettingsNameEnum.auth_plugin.value]
    #     except Exception as e:
    #         Console.set_foreground_color(ForegroundColorEnum.red)
    #         Console.write_line(f"[ ERROR ] [ {__name__} ]: Reading error in {type(self).__name__} settings")
    #         Console.write_line(f"[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}")
    #         Console.set_foreground_color(ForegroundColorEnum.default)
