import os

from cpl_cli import Error
from cpl_cli.configuration import WorkspaceSettings, ProjectSettings
from cpl_core.configuration import ConfigurationABC
from cpl_core.configuration.validator_abc import ValidatorABC
from cpl_core.environment import ApplicationEnvironmentABC


class ProjectValidator(ValidatorABC):
    def __init__(
        self,
        config: ConfigurationABC,
        env: ApplicationEnvironmentABC,
        workspace: WorkspaceSettings,
        project: ProjectSettings,
    ):
        self._config: ConfigurationABC = config
        self._env: ApplicationEnvironmentABC = env
        self._workspace: WorkspaceSettings = workspace
        self._project: ProjectSettings = project

        ValidatorABC.__init__(self)

    def validate(self) -> bool:
        if self._project is None and self._workspace is not None:
            project = self._workspace.projects[self._workspace.default_project]
            self._config.add_json_file(project, optional=True, output=False)
            self._project = self._config.get_configuration(ProjectSettings)
            self._env.set_working_directory(os.path.join(self._env.working_directory, os.path.dirname(project)))

        result = self._project is not None or self._workspace is not None
        if not result:
            Error.error("The command requires to be run in an CPL project, but a project could not be found.")
        return result
