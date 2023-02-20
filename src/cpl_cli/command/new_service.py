import importlib
import os
import sys
import textwrap
import traceback
from typing import Optional

from packaging import version

import cpl_cli
import cpl_core
from cpl_cli.abc.project_type_abc import ProjectTypeABC
from cpl_cli.command_abc import CommandABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.build_settings_name_enum import BuildSettingsNameEnum
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_settings_name_enum import ProjectSettingsNameEnum
from cpl_cli.configuration.project_type_enum import ProjectTypeEnum
from cpl_cli.configuration.venv_helper_service import VenvHelper
from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum
from cpl_cli.configuration.workspace_settings import WorkspaceSettings
from cpl_cli.helper.dependencies import Dependencies
from cpl_cli.source_creator.template_builder import TemplateBuilder
from cpl_core.configuration.configuration_abc import ConfigurationABC
from cpl_core.console.console import Console
from cpl_core.console.foreground_color_enum import ForegroundColorEnum
from cpl_core.utils.string import String


class NewService(CommandABC):
    def __init__(self, configuration: ConfigurationABC):
        """
        Service for the CLI command new
        :param configuration:
        """
        CommandABC.__init__(self)

        self._config = configuration
        self._env = self._config.environment

        self._workspace: WorkspaceSettings = self._config.get_configuration(WorkspaceSettings)
        self._project: ProjectSettings = ProjectSettings()
        self._project_dict = {}
        self._build: BuildSettings = BuildSettings()
        self._build_dict = {}

        self._project_type_classes = set()

        self._name: str = ""
        self._rel_path: str = ""
        self._project_type: ProjectTypeEnum = ProjectTypeEnum.console
        self._use_nothing: bool = False
        self._use_application_api: bool = False
        self._use_startup: bool = False
        self._use_service_providing: bool = False
        self._use_async: bool = False
        self._use_venv: bool = False
        self._use_base: bool = False

    @property
    def help_message(self) -> str:
        return textwrap.dedent(
            """\
        Generates a workspace and initial project or add a project to workspace.
        Usage: cpl new <type> <name>
        
        Arguments:
            type        The project type of the initial project
            name        Name of the workspace or the project
            
        Types:
            console (c|C)
            library (l|L)
            unittest (ut|UT)
        """
        )

    def _create_project_settings(self):
        self._rel_path = os.path.dirname(self._name)
        self._project_dict = {
            ProjectSettingsNameEnum.name.value: os.path.basename(self._name),
            ProjectSettingsNameEnum.version.value: {
                VersionSettingsNameEnum.major.value: "0",
                VersionSettingsNameEnum.minor.value: "0",
                VersionSettingsNameEnum.micro.value: "0",
            },
            ProjectSettingsNameEnum.author.value: "",
            ProjectSettingsNameEnum.author_email.value: "",
            ProjectSettingsNameEnum.description.value: "",
            ProjectSettingsNameEnum.long_description.value: "",
            ProjectSettingsNameEnum.url.value: "",
            ProjectSettingsNameEnum.copyright_date.value: "",
            ProjectSettingsNameEnum.copyright_name.value: "",
            ProjectSettingsNameEnum.license_name.value: "",
            ProjectSettingsNameEnum.license_description.value: "",
            ProjectSettingsNameEnum.dependencies.value: [f"cpl-core>={version.parse(cpl_core.__version__)}"],
            ProjectSettingsNameEnum.dev_dependencies.value: [f"cpl-cli>={version.parse(cpl_cli.__version__)}"],
            ProjectSettingsNameEnum.python_version.value: f'>={sys.version.split(" ")[0]}',
            ProjectSettingsNameEnum.python_path.value: {sys.platform: "../../venv/" if self._use_venv else ""},
            ProjectSettingsNameEnum.classifiers.value: [],
        }

        self._project.from_dict(self._project_dict)

    def _create_build_settings(self, project_type: str):
        self._build_dict = {
            BuildSettingsNameEnum.project_type.value: project_type,
            BuildSettingsNameEnum.source_path.value: "",
            BuildSettingsNameEnum.output_path.value: "../../dist",
            BuildSettingsNameEnum.main.value: f"{String.convert_to_snake_case(self._project.name)}.main",
            BuildSettingsNameEnum.entry_point.value: self._project.name,
            BuildSettingsNameEnum.include_package_data.value: False,
            BuildSettingsNameEnum.included.value: [],
            BuildSettingsNameEnum.excluded.value: ["*/__pycache__", "*/logs", "*/tests"],
            BuildSettingsNameEnum.package_data.value: {},
            BuildSettingsNameEnum.project_references.value: [],
        }
        self._build.from_dict(self._build_dict)

    def _create_project_json(self):
        """
        Creates cpl.json content
        :return:
        """
        self._project_json = {ProjectSettings.__name__: self._project_dict, BuildSettings.__name__: self._build_dict}

    def _get_project_path(self) -> Optional[str]:
        """
        Gets project path
        :return:
        """
        if self._workspace is None:
            project_path = os.path.join(self._env.working_directory, self._rel_path, self._project.name)
        else:
            base = "" if self._use_base else "src"
            project_path = os.path.join(
                self._env.working_directory, base, self._rel_path, String.convert_to_snake_case(self._project.name)
            )

        if os.path.isdir(project_path) and len(os.listdir(project_path)) > 0:
            Console.write_line(project_path)
            Console.error("Project path is not empty\n")
            return None

        return project_path

    def _get_project_information(self, project_type: str):
        """
        Gets project information's from user
        :return:
        """
        is_unittest = project_type == "unittest"
        is_library = project_type == "library"
        if is_library:
            return

        if (
            self._use_application_api
            or self._use_startup
            or self._use_service_providing
            or self._use_async
            or self._use_nothing
        ):
            Console.set_foreground_color(ForegroundColorEnum.default)
            Console.write_line("Skipping question due to given flags")
            return

        if not is_unittest and not is_library:
            self._use_application_api = Console.read("Do you want to use application base? (y/n) ").lower() == "y"

        if not is_unittest and self._use_application_api:
            self._use_startup = Console.read("Do you want to use startup? (y/n) ").lower() == "y"

        if not is_unittest and not self._use_application_api:
            self._use_service_providing = Console.read("Do you want to use service providing? (y/n) ").lower() == "y"

        if not self._use_async:
            self._use_async = Console.read("Do you want to use async? (y/n) ").lower() == "y"

        Console.set_foreground_color(ForegroundColorEnum.default)

    def _create_venv(self):
        project = self._project.name
        if self._workspace is not None:
            project = self._workspace.default_project

        if self._env.working_directory.endswith(project):
            project = ""

        if self._workspace is None and self._use_base:
            project = f"{self._rel_path}/{project}"

        VenvHelper.init_venv(
            False,
            self._env,
            self._project,
            explicit_path=os.path.join(
                self._env.working_directory, project, self._project.python_executable.replace("../", "")
            ),
        )

    def _read_custom_project_types_from_path(self, path: str):
        if not os.path.exists(os.path.join(path, ".cpl")):
            return

        sys.path.insert(0, os.path.join(path, ".cpl"))
        for r, d, f in os.walk(os.path.join(path, ".cpl")):
            for file in f:
                if file.startswith("project_file_") or not file.startswith("project_") or not file.endswith(".py"):
                    continue

                try:
                    exec(open(os.path.join(r, file), "r").read())
                    self._project_type_classes.update(ProjectTypeABC.__subclasses__())
                except Exception as e:
                    Console.error(str(e), traceback.format_exc())
                    sys.exit(-1)

    def _create_project(self, project_type: str):
        for package_name in Dependencies.get_cpl_packages():
            if package_name == "cpl-cli":
                continue
            package = importlib.import_module(String.convert_to_snake_case(package_name[0]))
            self._read_custom_project_types_from_path(os.path.dirname(package.__file__))

        self._read_custom_project_types_from_path(self._env.working_directory)
        self._read_custom_project_types_from_path(self._env.runtime_directory)

        if len(self._project_type_classes) == 0:
            Console.error(f"No project types found in template directory: .cpl")
            sys.exit()

        project_class = None
        known_project_types = []
        for p in self._project_type_classes:
            known_project_types.append(p.__name__)
            if p.__name__.lower() != project_type and p.__name__.lower()[0] != project_type[0]:
                continue

            project_class = p

        if project_class is None:
            Console.error(f"Project type {project_type} not found in template directory: .cpl/")
            sys.exit()

        project_type = String.convert_to_snake_case(project_class.__name__)
        self._create_project_settings()
        self._create_build_settings(project_type)
        self._create_project_json()
        path = self._get_project_path()
        if path is None:
            return

        self._get_project_information(project_type)
        project_name = self._project.name
        if self._rel_path != "":
            project_name = f"{self._rel_path}/{project_name}"

        base = "src/"
        split_project_name = project_name.split("/")
        if self._use_base and len(split_project_name) > 0:
            base = f"{split_project_name[0]}/"

        project = project_class(
            base if self._workspace is not None else "src/",
            project_name,
            self._workspace,
            self._use_application_api,
            self._use_startup,
            self._use_service_providing,
            self._use_async,
            self._project_json,
        )

        if self._workspace is None:
            TemplateBuilder.create_workspace(
                f"{project_name}/cpl-workspace.json",
                project_name.split("/")[-1],
                {
                    project_name: f'{base if self._workspace is not None else "src/"}{String.convert_to_snake_case(project_name)}/{project_name}.json'
                },
                {},
            )
        else:
            self._workspace.projects[
                project_name
            ] = f'{base if self._workspace is not None else "src/"}{String.convert_to_snake_case(project_name)}/{project_name}.json'
            TemplateBuilder.create_workspace(
                "cpl-workspace.json", self._workspace.default_project, self._workspace.projects, self._workspace.scripts
            )

        for template in project.templates:
            rel_base = "/".join(project_name.split("/")[:-1])
            template_path_base = template.path.split("/")[0]
            if not self._use_base and rel_base != "" and template_path_base != "" and template_path_base != rel_base:
                template.path = template.path.replace(f"{template_path_base}/", f"{template_path_base}/{rel_base}/")

            if template.name.endswith(f'{project_name.split("/")[-1]}.json'):
                pass

            file_path = os.path.join(project_name if self._workspace is None else "", template.path, template.name)

            Console.spinner(
                f"Creating {file_path}",
                TemplateBuilder.build,
                file_path,
                template,
                text_foreground_color=ForegroundColorEnum.green,
                spinner_foreground_color=ForegroundColorEnum.cyan,
            )

        if self._use_venv:
            self._create_venv()

    def execute(self, args: list[str]):
        """
        Entry point of command
        :param args:
        :return:
        """
        if "nothing" in args:
            self._use_nothing = True
            self._use_async = False
            self._use_application_api = False
            self._use_startup = False
            self._use_service_providing = False
            if "async" in args:
                args.remove("async")
            if "application-base" in args:
                args.remove("application-base")
            if "startup" in args:
                args.remove("startup")
            if "service-providing" in args:
                args.remove("service-providing")

        if "async" in args:
            self._use_async = True
            args.remove("async")
        if "application-base" in args:
            self._use_application_api = True
            args.remove("application-base")
        if "startup" in args:
            self._use_startup = True
            args.remove("startup")
        if "service-providing" in args:
            self._use_service_providing = True
            args.remove("service-providing")
        if "venv" in args:
            self._use_venv = True
            args.remove("venv")
        if "base" in args:
            self._use_base = True
            args.remove("base")

        if len(args) <= 1:
            Console.error(f"Project type not found")
            Console.write_line(self.help_message)
            return

        self._name = args[1]
        self._create_project(args[0])
