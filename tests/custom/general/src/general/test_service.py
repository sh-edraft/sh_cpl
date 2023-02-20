from cpl_core.console.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.pipes.ip_address_pipe import IPAddressPipe


class TestService:
    def __init__(self, provider: ServiceProviderABC, ip_pipe: IPAddressPipe):
        self._provider = provider
        self._ip_pipe = ip_pipe

    def run(self):
        Console.write_line("Hello World!", self._provider)
        ip = [192, 168, 178, 30]
        Console.write_line(ip, self._ip_pipe.transform(ip))
