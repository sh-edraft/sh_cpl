from enum import Enum


class ServiceLifetimeEnum(Enum):

    singleton = 0
    scoped = 1  # not supported yet
    transient = 2
