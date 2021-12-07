from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class TableABC(ABC):

    @abstractmethod
    def __init__(self):
        self._created_at: Optional[datetime] = datetime.now().isoformat()
        self._modified_at: Optional[datetime] = datetime.now().isoformat()
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def modified_at(self) -> datetime:
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime):
        self._modified_at = value
    
    @property
    @abstractmethod
    def insert_string(self) -> str: pass
    
    @property
    @abstractmethod
    def udpate_string(self) -> str: pass
    
    @property
    @abstractmethod
    def delete_string(self) -> str: pass
