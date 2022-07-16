from abc import ABC, abstractmethod
from typing import Type

from cpl_query.extension import List

from cpl_cli import CommandABC


class DiscordCollectionABC(ABC):

    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def add_command(self, _t: Type[CommandABC]): pass

    @abstractmethod
    def add_event(self, _t_event: Type, _t: Type): pass

    @abstractmethod
    def get_events_by_base(self, _t_event: Type): pass
