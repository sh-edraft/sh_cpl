from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.dependency_injection.service_descriptor import ServiceDescriptor
from cpl.dependency_injection.service_factory_abc import ServiceFactoryABC


class ServiceFactory(ServiceFactoryABC):

    def __init__(self, service_descriptors: list[ServiceDescriptor], config: ConfigurationABC,
                 runtime: ApplicationRuntimeABC):
        ServiceFactoryABC.__init__(self)

        self._service_descriptors: list[ServiceDescriptor] = service_descriptors
        self._configuration: ConfigurationABC = config
        self._runtime: ApplicationRuntimeABC = runtime

    @property
    def service_descriptors(self) -> list[ServiceDescriptor]:
        return self._service_descriptors

    @property
    def configuration(self) -> ConfigurationABC:
        return self._configuration

    @property
    def runtime(self) -> ApplicationRuntimeABC:
        return self._runtime
