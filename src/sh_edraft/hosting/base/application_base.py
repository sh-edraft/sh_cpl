from abc import ABC, abstractmethod


class ApplicationBase(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    def create_configuration(self): pass

    @abstractmethod
    def create_services(self): pass

    @abstractmethod
    def main(self): pass
