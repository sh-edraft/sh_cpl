from socket import gethostname
from typing import Optional

from cpl.environment.environment_abc import EnvironmentABC
from cpl.environment.environment_name_enum import EnvironmentName


class HostingEnvironment(EnvironmentABC):

    def __init__(self, name: EnvironmentName = EnvironmentName.production, crp: str = './'):
        EnvironmentABC.__init__(self)

        self._environment_name: Optional[EnvironmentName] = name
        self._app_name: Optional[str] = None
        self._customer: Optional[str] = None
        self._content_root_path: Optional[str] = crp

    @property
    def environment_name(self) -> str:
        return str(self._environment_name.value)

    @environment_name.setter
    def environment_name(self, environment_name: str):
        self._environment_name = EnvironmentName(environment_name)

    @property
    def application_name(self) -> str:
        return self._app_name if self._app_name is not None else ''

    @application_name.setter
    def application_name(self, application_name: str):
        self._app_name = application_name

    @property
    def customer(self) -> str:
        return self._customer if self._customer is not None else ''

    @customer.setter
    def customer(self, customer: str):
        self._customer = customer

    @property
    def content_root_path(self) -> str:
        return self._content_root_path

    @content_root_path.setter
    def content_root_path(self, content_root_path: str):
        self._content_root_path = content_root_path

    @property
    def host_name(self):
        return gethostname()
