from enum import Enum


class DatabaseSettingsName(Enum):

    connection_string = 'ConnectionString'
    credentials = 'Credentials'
    encoding = 'Encoding'
    case_sensitive = 'CaseSensitive'
    echo = 'Echo'
    auth_plugin = 'AuthPlugin'
