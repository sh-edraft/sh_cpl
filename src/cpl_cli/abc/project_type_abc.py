from abc import ABC, abstractmethod
from typing import Optional

from cpl_cli.abc.file_template_abc import FileTemplateABC
from cpl_cli.configuration import WorkspaceSettings


class ProjectTypeABC(ABC):
    @abstractmethod
    def __init__(
        self,
        base_path: str,
        project_name: str,
        workspace: Optional[WorkspaceSettings],
        use_application_api: bool,
        use_startup: bool,
        use_service_providing: bool,
        use_async: bool,
        project_file_data: dict,
    ):
        self._templates: list[FileTemplateABC] = []
        self._base_path = base_path
        self._project_name = project_name
        self._workspace = workspace
        self._use_application_api = use_application_api
        self._use_startup = use_startup
        self._use_service_providing = use_service_providing
        self._use_async = use_async
        self._project_file_data = project_file_data

    @property
    def templates(self) -> list[FileTemplateABC]:
        return self._templates

    def add_template(self, t: FileTemplateABC):
        self._templates.append(t)
