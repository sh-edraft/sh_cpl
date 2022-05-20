from cpl_cli import Error
from cpl_cli.configuration import WorkspaceSettings, ProjectSettings
from cpl_core.configuration.validator_abc import ValidatorABC


class ProjectValidator(ValidatorABC):

    def __init__(self, workspace: WorkspaceSettings, project: ProjectSettings):
        self._workspace = workspace
        self._project = project

        ValidatorABC.__init__(self)

    def validate(self) -> bool:
        result = self._project is not None or self._workspace is not None
        if not result:
            Error.error('The command requires to be run in an CPL project, but a project could not be found.')
        return result
