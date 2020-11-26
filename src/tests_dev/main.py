import sys

from sh_edraft.hosting import ApplicationHost
from sh_edraft.hosting.base.application_base import ApplicationBase


class Program(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)

        self._app_host = ApplicationHost('CPL_DEV_Test', sys.argv)
        self._config = self._app_host.services.config
        self._services = self._app_host.services

    def create_configuration(self):
        self._config.create()

    def create_services(self):
        self._services.create()

    def main(self):
        print('RUN')


if __name__ == '__main__':
    program = Program()
    program.create_configuration()
    program.create_services()
    program.main()
