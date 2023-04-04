import os
from typing import Optional

from cpl_cli.command.custom_script_service import CustomScriptService
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_core.application.startup_extension_abc import StartupExtensionABC
from cpl_core.configuration.argument_type_enum import ArgumentTypeEnum
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.dependency_injection.service_collection_abc import ServiceCollectionABC
from cpl_core.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_core.utils.string import String


class StartupWorkspaceExtension(StartupExtensionABC):
    def __init__(self):
        pass

    @staticmethod
    def _search_project_json(working_directory: str) -> Optional[str]:
        project_name = None
        name = os.path.basename(working_directory)
        for r, d, f in os.walk(working_directory):
            for file in f:
                if file.endswith(".json"):
                    f_name = file.split(".json")[0]
                    if (
                        f_name == name
                        or String.convert_to_camel_case(f_name).lower() == String.convert_to_camel_case(name).lower()
                    ):
                        project_name = f_name
                        break

        return project_name

    def _read_cpl_environment(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        workspace: Optional[WorkspaceSettings] = config.get_configuration(WorkspaceSettings)
        config.add_configuration("PATH_WORKSPACE", env.working_directory)
        if workspace is not None:
            for script in workspace.scripts:
                config.create_console_argument(ArgumentTypeEnum.Executable, "", script, [], CustomScriptService)
            return

        project = self._search_project_json(env.working_directory)
        if project is not None:
            project = f"{project}.json"

        if project is None:
            return

        config.add_json_file(project, optional=True, output=False)

    def configure_configuration(self, config: ConfigurationABC, env: ApplicationEnvironmentABC):
        config.add_json_file("cpl-workspace.json", path=env.working_directory, optional=True, output=False)
        self._read_cpl_environment(config, env)

    def configure_services(self, services: ServiceCollectionABC, env: ApplicationEnvironmentABC):
        pass
