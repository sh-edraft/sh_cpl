from typing import Type

from sh_edraft.service.base.service_base import ServiceBase


class ProvideState:

    def __init__(self, service: Type[ServiceBase] = None, args: tuple = None):
        self._service: Type[ServiceBase] = service
        self._args: tuple = args

    @property
    def service(self):
        return self._service

    @property
    def args(self) -> tuple:
        return self._args
