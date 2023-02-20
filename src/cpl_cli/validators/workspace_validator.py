from cpl_cli import Error
from cpl_cli.configuration import WorkspaceSettings
from cpl_core.configuration.validator_abc import ValidatorABC


class WorkspaceValidator(ValidatorABC):
    def __init__(self, workspace: WorkspaceSettings):
        self._workspace = workspace

        ValidatorABC.__init__(self)

    def validate(self) -> bool:
        result = self._workspace is not None
        if not result:
            Error.error("The command requires to be run in an CPL workspace, but a workspace could not be found.")
        return result
