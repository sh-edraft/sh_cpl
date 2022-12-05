import os

from cpl_cli.abc.project_type_abc import ProjectTypeABC
from cpl_cli.configuration import WorkspaceSettings
from cpl_core.utils import String


class Console(ProjectTypeABC):

    def __init__(
            self,
            base_path: str,
            project_name: str,
            workspace: WorkspaceSettings,
            use_application_api: bool,
            use_startup: bool,
            use_service_providing: bool,
            use_async: bool,
    ):
        from project_file_license import ProjectFileLicense
        from project_file_readme import ProjectFileReadme
        from schematic_init import Init
        from project_file_code_application import ProjectFileApplication
        from project_file_code_main import ProjectFileMain
        from project_file_code_startup import ProjectFileStartup

        ProjectTypeABC.__init__(self, base_path, project_name, workspace, use_application_api, use_startup, use_service_providing, use_async)

        project_path = f'{base_path}{String.convert_to_snake_case(project_name.split("/")[-1])}/'

        self.add_template(ProjectFileLicense(''))
        self.add_template(ProjectFileReadme(''))
        self.add_template(Init('', 'init', f'{base_path}tests/'))
        self.add_template(Init('', 'init', project_path))

        if use_application_api:
            self.add_template(ProjectFileApplication(project_path, use_application_api, use_startup, use_service_providing, use_async))

        if use_startup:
            self.add_template(ProjectFileStartup(project_path, use_application_api, use_startup, use_service_providing, use_async))

        self.add_template(ProjectFileMain(project_path, use_application_api, use_startup, use_service_providing, use_async))
