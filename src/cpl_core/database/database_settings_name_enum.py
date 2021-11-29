from enum import Enum


class DatabaseSettingsNameEnum(Enum):

    host = 'Host'
    user = 'User'
    password = 'Password'
    database = 'Database'
    charset = 'Charset'
    use_unicode = 'UseUnicode'
    buffered = 'Buffered'
    auth_plugin = 'AuthPlugin'
