import os

from cpl_cli.abc.project_type_abc import ProjectTypeABC
from cpl_cli.configuration import WorkspaceSettings
from cpl_core.utils import String


class Library(ProjectTypeABC):

    def __init__(
            self,
            base_path: str,
            project_name: str,
            workspace: WorkspaceSettings,
            use_application_api: bool,
            use_startup: bool,
            use_service_providing: bool,
            use_async: bool,
            project_file_data: dict,
    ):
        from project_file import ProjectFile
        from project_file_readme import ProjectFileReadme
        from project_file_license import ProjectFileLicense
        from schematic_init import Init
        from schematic_class import Class

        ProjectTypeABC.__init__(self, base_path, project_name, workspace, use_application_api, use_startup, use_service_providing, use_async, project_file_data)

        project_path = f'{base_path}{String.convert_to_snake_case(project_name.split("/")[-1])}/'

        self.add_template(ProjectFile(project_name.split('/')[-1], project_path, project_file_data))
        if workspace is None:
            self.add_template(ProjectFileLicense(''))
            self.add_template(ProjectFileReadme(''))

        self.add_template(Init('', 'init', project_path))
        self.add_template(Class('Class1', 'class', project_path))
