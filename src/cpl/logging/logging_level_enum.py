from enum import Enum


class LoggingLevelEnum(Enum):

    OFF = 0         # Nothing
    FATAL = 1       # Error that cause exit
    ERROR = 2       # Non fatal error
    WARN = 3        # Error that can later be fatal
    INFO = 4        # Normal information's
    DEBUG = 5       # Detailed app state
    TRACE = 6       # Detailed app information's
