from cpl_core.application import StartupABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
from cpl_core.environment import ApplicationEnvironment
from cpl_discord import get_discord_collection
from cpl_discord.discord_event_types_enum import DiscordEventTypesEnum
from modules.hello_world.on_ready_event import OnReadyEvent
from modules.hello_world.on_ready_test_event import OnReadyTestEvent
from modules.hello_world.ping_command import PingCommand


class Startup(StartupABC):

    def __init__(self):
        StartupABC.__init__(self)

    def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
        configuration.add_json_file('appsettings.json', optional=True)
        configuration.add_environment_variables('CPL_')
        configuration.add_environment_variables('DISCORD_')

        return configuration

    def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
        services.add_logging()
        services.add_discord()
        dc_collection = get_discord_collection(services)
        dc_collection.add_event(DiscordEventTypesEnum.on_ready.value, OnReadyEvent)
        dc_collection.add_event(DiscordEventTypesEnum.on_ready.value, OnReadyTestEvent)
        dc_collection.add_command(PingCommand)

        return services.build_service_provider()
