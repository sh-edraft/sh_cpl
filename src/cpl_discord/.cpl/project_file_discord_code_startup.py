from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC
from cpl_core.utils import String


class DiscordBotProjectFileStartup(CodeFileTemplateABC):

    def __init__(self, project_name: str, path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool, use_async: bool):
        CodeFileTemplateABC.__init__(self, 'startup', path, '', use_application_api, use_startup, use_service_providing, use_async)
        self._project_name = project_name

    def get_code(self) -> str:
        import textwrap

        import_pkg = f'{String.convert_to_snake_case(self._project_name)}.'

        return textwrap.dedent(f"""\
        from cpl_core.application import StartupABC
        from cpl_core.configuration import ConfigurationABC
        from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
        from cpl_core.environment import ApplicationEnvironment
        from cpl_discord import get_discord_collection
        from cpl_discord.discord_event_types_enum import DiscordEventTypesEnum
        from {import_pkg}commands.ping_command import PingCommand
        from {import_pkg}events.on_ready_event import OnReadyEvent
        
        
        class Startup(StartupABC):
        
            def __init__(self):
                StartupABC.__init__(self)
        
            def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
                configuration.add_json_file('appsettings.json', optional=False)
                configuration.add_environment_variables('CPL_')
                configuration.add_environment_variables('DISCORD_')
        
                return configuration
        
            def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
                services.add_logging()
                services.add_discord()
                dc_collection = get_discord_collection(services)
                dc_collection.add_event(DiscordEventTypesEnum.on_ready.value, OnReadyEvent)
                dc_collection.add_command(PingCommand)
        
                return services.build_service_provider()
        """)
