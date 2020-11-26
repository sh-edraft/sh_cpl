from typing import Optional

from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base import ApplicationBase


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host: Optional[ApplicationHost] = None

    def create_application_host(self):
        self._app_host = ApplicationHost('CPL_DEV_Test')

    def create_configuration(self):
        self._app_host.configuration.create()

    def create_services(self):
        self._app_host.services.create()

    def main(self):
        print('RUN')
