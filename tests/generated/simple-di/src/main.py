from cpl_core.configuration import Configuration, ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceCollection, ServiceProviderABC


def configure_configuration() -> ConfigurationABC:
    config = Configuration()
    return config


def configure_services(config: ConfigurationABC) -> ServiceProviderABC:
    services = ServiceCollection(config)
    return services.build_service_provider()


def main():
    config = configure_configuration()
    provider = configure_services(config)
    Console.write_line('Hello World')


if __name__ == '__main__':
    main()
