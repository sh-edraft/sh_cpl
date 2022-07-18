from enum import Enum


class DatabaseSettingsNameEnum(Enum):

    host = 'Host'
    port = 'Port'
    user = 'User'
    password = 'Password'
    database = 'Database'
    charset = 'Charset'
    use_unicode = 'UseUnicode'
    buffered = 'Buffered'
    auth_plugin = 'AuthPlugin'
