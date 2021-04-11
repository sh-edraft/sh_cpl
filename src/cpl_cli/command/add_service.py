import json
import os.path
from typing import Optional

from cpl.configuration.configuration_abc import ConfigurationABC
from cpl.console.console import Console
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.settings_helper import SettingsHelper
from cpl_cli.configuration.workspace_settings import WorkspaceSettings


class AddService(CommandABC):

    def __init__(self, config: ConfigurationABC, workspace: WorkspaceSettings):
        """
        Service for CLI command add
        """
        CommandABC.__init__(self)

        self._config = config

        self._workspace = workspace

    @staticmethod
    def _edit_project_file(source: str, project_settings: ProjectSettings, build_settings: BuildSettings):
        with open(source, 'w') as file:
            file.write(json.dumps({
                ProjectSettings.__name__: SettingsHelper.get_project_settings_dict(project_settings),
                BuildSettings.__name__: SettingsHelper.get_build_settings_dict(build_settings)
            }, indent=2))
            file.close()

    def run(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if len(args) == 0:
            Console.error('Expected source and target project')
            return

        elif len(args) == 1:
            Console.error('Expected target project')
            return

        elif len(args) > 2:
            Console.error(f'Unexpected argument: {" ".join(args[2:])}')
            return

        # file names
        source = args[0]
        target = args[1]
        # validation flags
        is_invalid_source = False
        is_invalid_target = source == target

        if not is_invalid_target:
            if self._workspace is None:
                is_invalid_source = not os.path.isfile(source)
                is_invalid_target = not os.path.isfile(target)

            else:
                if source not in self._workspace.projects:
                    is_invalid_source = True

                else:
                    source = self._workspace.projects[source]

                if target not in self._workspace.projects:
                    is_invalid_target = True

                else:
                    target = self._workspace.projects[target]

        # load project-name.json
        self._config.add_json_file(source, optional=True, output=False)
        project_settings: Optional[ProjectSettings] = self._config.get_configuration(ProjectSettings)
        build_settings: Optional[BuildSettings] = self._config.get_configuration(BuildSettings)

        if project_settings is None or build_settings is None:
            is_invalid_source = True

        if is_invalid_source:
            Console.error(f'Invalid source: {source}')
            return

        if is_invalid_target or source == target or not os.path.isfile(target):
            Console.error(f'Invalid target: {target}')
            return

        if target in build_settings.project_references:
            Console.error(f'Project reference already exists.')
            return

        if self._workspace is None:
            target = f'../{target}'
        else:
            target = target.replace('src', '..')

        build_settings.project_references.append(target)

        Console.spinner(
            f'Editing {source}',
            self._edit_project_file,
            source,
            project_settings,
            build_settings,
            text_foreground_color=ForegroundColorEnum.green,
            spinner_foreground_color=ForegroundColorEnum.cyan
        )
