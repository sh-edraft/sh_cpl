import os
import shutil
import time
from string import Template as stringTemplate

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.console.console import Console
from cpl_cli.publish.project_settings import ProjectSettings
from cpl_cli.publish.publisher_abc import PublisherABC


class Publisher(PublisherABC):

    def __init__(self, runtime: ApplicationRuntimeABC, project: ProjectSettings):
        PublisherABC.__init__(self)

        self._runtime = runtime
        self._project = project
        self._project.source_path = os.path.join(self._runtime.working_directory, self._project.source_path)
        self._project.dist_path = os.path.join(self._runtime.working_directory, self._project.dist_path)

        self._included_files: list[str] = []

    @property
    def source_path(self) -> str:
        return ''

    @property
    def dist_path(self) -> str:
        return ''

    @staticmethod
    def _get_module_name_from_dirs(file: str) -> str:
        dirs = os.path.dirname(file).split('/')
        for d in dirs:
            if d.__contains__('.'):
                dirs.remove(d)

        if len(dirs) == 0:
            return os.path.basename(file)
        else:
            return '.'.join(dirs)

    @staticmethod
    def _delete_path(path: str):
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                Console.error(f'{e}')
                exit()

    @staticmethod
    def _create_path(path: str):
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except Exception as e:
                Console.error(f'{e}')
                exit()

    def _read_sources(self):
        time.sleep(2)
        for file in self._project.included:
            rel_path = os.path.relpath(file)
            if os.path.isdir(rel_path):
                for r, d, f in os.walk(rel_path):
                    for sub_file in f:
                        relative_path = os.path.relpath(r)
                        file_path = os.path.join(relative_path, os.path.relpath(sub_file))

                        is_excluded = False
                        for excluded in self._project.excluded:
                            if excluded in relative_path:
                                is_excluded = True

                            if relative_path in excluded:
                                is_excluded = True

                        if not is_excluded:
                            self._included_files.append(os.path.relpath(file_path))

            elif os.path.isfile(rel_path):
                self._included_files.append(rel_path)

            else:
                Console.error(f'Path not found: {rel_path}')

        for r, d, f in os.walk(self._project.source_path):
            for file in f:
                relative_path = os.path.relpath(r)
                file_path = os.path.join(relative_path, os.path.relpath(file))

                if relative_path not in self._project.excluded:
                    self._included_files.append(os.path.relpath(file_path))

    def _create_packages(self):
        for file in self._included_files:
            if file.endswith('__init__.py'):
                template_content = ''
                module_file_lines: list[str] = []

                title = self._get_module_name_from_dirs(file)
                if title == '':
                    title = self._project.name
                elif not title.__contains__('.'):
                    title = f'{self._project.name}.{title}'

                module_py_lines: list[str] = []
                imports = ''

                with open(file, 'r') as py_file:
                    module_file_lines = py_file.readlines()
                    py_file.close()

                if len(module_file_lines) == 0:
                    imports = '# imports:'
                else:
                    is_started = False
                    for line in module_file_lines:
                        if line.__contains__('# imports'):
                            is_started = True

                        if (line.__contains__('from') or line.__contains__('import')) and is_started:
                            module_py_lines.append(line.replace('\n', ''))

                    if len(module_py_lines) > 0:
                        imports = '\n'.join(module_py_lines)

                with open(os.path.join(self._runtime.runtime_directory, 'templates/build/init.txt'), 'r') as template:
                    template_content = stringTemplate(template.read()).substitute(
                        Name=self._project.name,
                        Description=self._project.description,
                        LongDescription=self._project.long_description,
                        CopyrightDate=self._project.copyright_date,
                        CopyrightName=self._project.copyright_name,
                        LicenseName=self._project.license_name,
                        LicenseDescription=self._project.license_description,
                        Title=title if title is not None and title != '' else self._project.name,
                        Author=self._project.author,
                        Version=self._project.version.to_str(),
                        Major=self._project.version.major,
                        Minor=self._project.version.minor,
                        Micro=self._project.version.micro,
                        Imports=imports
                    )

                with open(file, 'w+') as py_file:
                    py_file.write(template_content)
                    py_file.close()

    def _dist_files(self):
        build_path = os.path.join(self._project.dist_path, 'build')
        self._delete_path(build_path)
        self._create_path(build_path)

        for file in self._included_files:
            output_path = os.path.join(build_path, os.path.dirname(file))
            output_file = os.path.join(build_path, file)

            try:
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
            except Exception as e:
                Console.error(__name__, f'Cannot create directories: {output_path} -> {e}')

            try:
                shutil.copy(os.path.abspath(file), output_file)
            except Exception as e:
                Console.error(__name__, f'Cannot copy file: {file} to {output_path} -> {e}')

    def include(self, path: str):
        self._project.included.append(path)

    def exclude(self, path: str):
        self._project.excluded.append(path)

    def build(self):
        Console.spinner('Reading source files:', self._read_sources)
        Console.spinner('Creating internal packages:', self._create_packages)
        Console.write_line('Building application:')
        self._dist_files()

    def publish(self):
        pass
