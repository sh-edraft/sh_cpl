# Using cpl g & cpl n templating

## Contents

- [Prerequisites](#prerequisites)
- [Generate schematics](#cpl-generate-scmatics)
- [Project types](#cpl-new-project-types)

## Prerequisites

Create a folder called ```.cpl```

## cpl generate schematics

Create a file which begins with ```schematic_your_schematic.py```.
A schematic template is detected by starting with  ```schematic_``` and endswith ```.py```.

You should replace ```your_schematic``` with an appropriate name of your schematic. For example, we will choose ```Enum```.
Attention: It is important that you do not overwrite templates by creating a file or class with the same name.

In the template create a class with the name of your schematic. For example:

```python
from cpl_cli.abc.generate_schematic_abc import GenerateSchematicABC


class Enum(GenerateSchematicABC):

    def __init__(self, *args: str):
        GenerateSchematicABC.__init__(self, *args)

    def get_code(self) -> str:
        import textwrap
        code = textwrap.dedent("""\
        from enum import Enum
        
        
        class $Name(Enum):
        
            atr = 0
        """)
        return self.build_code_str(code, Name=self._class_name)

    @classmethod
    def register(cls):
        GenerateSchematicABC.register(
            cls,
            'enum',
            ['e', 'E']
        )

```

You can test it by calling ```cpl g --help``` your schematic should be listed as available.

## cpl new project types

The project templating is a little more complex and is therefore divided into several files.
First of all, for information, it is very important not to overwrite any existing files or classes!

Template structure explained by the example of the internal type ```console```:

```
- project_console.py
- project_file_license.py
- project_file_appsettings.py
- project_file.py
- project_file_readme.py
- project_file_code_main.py
- project_file_code_startup.py
- project_file_code_application.py
```

Here the template ```project_console.py``` defines how a console project has to look like when it is generated. Here is the code to illustrate this:

```python
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
            project_file_data: dict,
    ):
        from project_file import ProjectFile
        from project_file_appsettings import ProjectFileAppsettings
        from project_file_code_application import ProjectFileApplication
        from project_file_code_main import ProjectFileMain
        from project_file_code_startup import ProjectFileStartup
        from project_file_readme import ProjectFileReadme
        from project_file_license import ProjectFileLicense
        from schematic_init import Init

        ProjectTypeABC.__init__(self, base_path, project_name, workspace, use_application_api, use_startup, use_service_providing, use_async, project_file_data)

        project_path = f'{base_path}{String.convert_to_snake_case(project_name.split("/")[-1])}/'

        self.add_template(ProjectFile(project_name.split('/')[-1], project_path, project_file_data))
        if workspace is None:
            self.add_template(ProjectFileLicense(''))
            self.add_template(ProjectFileReadme(''))
            self.add_template(Init('', 'init', f'{base_path}tests/'))

        self.add_template(Init('', 'init', project_path))
        self.add_template(ProjectFileAppsettings(project_path))

        if use_application_api:
            self.add_template(ProjectFileApplication(project_path, use_application_api, use_startup, use_service_providing, use_async))

        if use_startup:
            self.add_template(ProjectFileStartup(project_path, use_application_api, use_startup, use_service_providing, use_async))

        self.add_template(ProjectFileMain(project_name.split('/')[-1], project_path, use_application_api, use_startup, use_service_providing, use_async))
```

The class must be named exactly as the project type should be named. It is also checked on the initial letter of the class as alias.
Now create a class for normal files which inherits from ```FileTemplateABC``` and a class for code files which inherits from ```CodeFileTemplateABC```.

For example:

project_file_code_startup.py:
```python
from cpl_cli.abc.code_file_template_abc import CodeFileTemplateABC


class ProjectFileStartup(CodeFileTemplateABC):

    def __init__(self, path: str, use_application_api: bool, use_startup: bool, use_service_providing: bool, use_async: bool):
        CodeFileTemplateABC.__init__(self, 'startup', path, '', use_application_api, use_startup, use_service_providing, use_async)

    def get_code(self) -> str:
        import textwrap

        return textwrap.dedent("""\
        from cpl_core.application import StartupABC
        from cpl_core.configuration import ConfigurationABC
        from cpl_core.dependency_injection import ServiceProviderABC, ServiceCollectionABC
        from cpl_core.environment import ApplicationEnvironment
        
        
        class Startup(StartupABC):
        
            def __init__(self):
                StartupABC.__init__(self)
        
            def configure_configuration(self, configuration: ConfigurationABC, environment: ApplicationEnvironment) -> ConfigurationABC:
                return configuration
        
            def configure_services(self, services: ServiceCollectionABC, environment: ApplicationEnvironment) -> ServiceProviderABC:
                return services.build_service_provider()
        """)
```

project_file.py:

```python
import json

from cpl_cli.abc.file_template_abc import FileTemplateABC


class ProjectFile(FileTemplateABC):

    def __init__(self, name: str, path: str, code: dict):
        FileTemplateABC.__init__(self, '', path, '{}')
        self._name = f'{name}.json'
        self._code = code

    def get_code(self) -> str:
        return json.dumps(self._code, indent=2)
```
