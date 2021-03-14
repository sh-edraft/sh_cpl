import importlib
import os
import shutil
from string import Template as stringTemplate

import setuptools
from packaging import version
from setuptools import sandbox

from cpl.application.application_runtime_abc import ApplicationRuntimeABC
from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.publish.publisher_abc import PublisherABC
from cpl_cli.templates.build.init_template import InitTemplate
from cpl_cli.templates.publish.setup_template import SetupTemplate


class PublisherService(PublisherABC):

    def __init__(self, runtime: ApplicationRuntimeABC, project: ProjectSettings, build: BuildSettings):
        PublisherABC.__init__(self)

        self._runtime = runtime
        self._project_settings = project
        self._build_settings = build

        self._source_path = os.path.join(self._runtime.working_directory, self._build_settings.source_path)
        self._output_path = os.path.join(self._runtime.working_directory, self._build_settings.output_path)

        self._included_files: list[str] = []
        self._included_dirs: list[str] = []
        self._distributed_files: list[str] = []

    @property
    def source_path(self) -> str:
        return ''

    @property
    def dist_path(self) -> str:
        return ''

    @staticmethod
    def _get_module_name_from_dirs(file: str) -> str:
        if 'src/' in file:
            file = file.replace('src/', '', 1)

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

    def _is_path_included(self, path: str) -> bool:
        for included in self._build_settings.included:
            if included.startswith('*'):
                included = included.replace('*', '')

            if included in path and path not in self._build_settings.excluded:
                return True

        return False

    def _is_path_excluded(self, path: str) -> bool:
        for excluded in self._build_settings.excluded:
            if excluded.startswith('*'):
                excluded = excluded.replace('*', '')

            if excluded in path and not self._is_path_included(path):
                return True

        return False

    def _read_sources(self):
        for file in self._build_settings.included:
            rel_path = os.path.relpath(file)
            if os.path.isdir(rel_path):
                for r, d, f in os.walk(rel_path):
                    for sub_file in f:
                        relative_path = os.path.relpath(r)
                        file_path = os.path.join(relative_path, os.path.relpath(sub_file))

                        self._included_files.append(os.path.relpath(file_path))

            elif os.path.isfile(rel_path):
                self._included_files.append(rel_path)

        for r, d, f in os.walk(self._build_settings.source_path):
            for file in f:
                relative_path = os.path.relpath(r)
                file_path = os.path.join(relative_path, os.path.relpath(file))

                if len(d) > 0:
                    for directory in d:
                        empty_dir = os.path.join(os.path.dirname(file_path), directory)
                        if len(os.listdir(empty_dir)) == 0:
                            self._included_dirs.append(empty_dir)

                if not self._is_path_excluded(relative_path):
                    self._included_files.append(os.path.relpath(file_path))

    def _create_packages(self):
        for file in self._included_files:
            if file.endswith('__init__.py'):
                template_content = ''
                module_file_lines: list[str] = []

                title = self._get_module_name_from_dirs(file)
                if title == '':
                    title = self._project_settings.name
                elif not title.__contains__('.'):
                    title = f'{self._project_settings.name}.{title}'

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

                template_content = stringTemplate(InitTemplate.get_init_py()).substitute(
                    Name=self._project_settings.name,
                    Description=self._project_settings.description,
                    LongDescription=self._project_settings.long_description,
                    CopyrightDate=self._project_settings.copyright_date,
                    CopyrightName=self._project_settings.copyright_name,
                    LicenseName=self._project_settings.license_name,
                    LicenseDescription=self._project_settings.license_description,
                    Title=title if title is not None and title != '' else self._project_settings.name,
                    Author=self._project_settings.author,
                    Version=version.parse(self._project_settings.version.to_str()),
                    Major=self._project_settings.version.major,
                    Minor=self._project_settings.version.minor,
                    Micro=self._project_settings.version.micro,
                    Imports=imports
                )

                with open(file, 'w+') as py_file:
                    py_file.write(template_content)
                    py_file.close()

    def _dist_files(self):
        build_path = os.path.join(self._output_path)
        self._delete_path(build_path)
        self._create_path(build_path)

        for file in self._included_files:
            dist_file = file
            if 'src/' in dist_file:
                dist_file = dist_file.replace('src/', '', 1)

            output_path = os.path.join(build_path, os.path.dirname(dist_file))
            output_file = os.path.join(build_path, dist_file)

            try:
                if not os.path.isdir(output_path):
                    os.makedirs(output_path, exist_ok=True)
            except Exception as e:
                Console.error(__name__, f'Cannot create directories: {output_path} -> {e}')
                return

            try:
                self._distributed_files.append(output_file)
                shutil.copy(os.path.abspath(file), output_file)
            except Exception as e:
                Console.error(__name__, f'Cannot copy file: {file} to {output_path} -> {e}')
                return

        for empty_dir in self._included_dirs:
            dist_dir = empty_dir
            if 'src/' in dist_dir:
                dist_dir = dist_dir.replace('src/', '', 1)

            output_path = os.path.join(build_path, dist_dir)
            if not os.path.isdir(output_path):
                os.makedirs(output_path)

    def _clean_dist_files(self):
        paths: list[str] = []
        for file in self._distributed_files:
            paths.append(os.path.dirname(file))

            if os.path.isfile(file):
                os.remove(file)

        for path in paths:
            if os.path.isdir(path):
                shutil.rmtree(path)

    @staticmethod
    def _package_files(directory):
        paths = []
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
        return paths

    def _create_setup(self):
        setup_file = os.path.join(self._output_path, 'setup.py')
        if os.path.isfile(setup_file):
            os.remove(setup_file)

        main = None
        try:
            main = importlib.import_module(self._build_settings.main)
        except Exception as e:
            Console.error('Could not find entry point', str(e))

        if main is None:
            Console.error('Could not find entry point')
            return

        with open(setup_file, 'w+') as setup_py:
            setup_string = stringTemplate(SetupTemplate.get_setup_py()).substitute(
                Name=self._project_settings.name,
                Version=self._project_settings.version.to_str(),
                Packages=setuptools.find_packages(where=self._output_path, exclude=self._build_settings.excluded),
                URL=self._project_settings.url,
                LicenseName=self._project_settings.license_name,
                Author=self._project_settings.author,
                AuthorMail=self._project_settings.author_email,
                IncludePackageData=self._build_settings.include_package_data,
                Description=self._project_settings.description,
                PyRequires=self._project_settings.python_version,
                Dependencies=self._project_settings.dependencies,
                EntryPoints={
                    'console_scripts': [
                        f'{self._build_settings.entry_point} = {main.__name__}:{main.main.__name__}'
                    ]
                },
                PackageData=self._build_settings.package_data
            )
            setup_py.write(setup_string)
            setup_py.close()

    def _run_setup(self):
        setup_py = os.path.join(self._output_path, 'setup.py')
        if not os.path.isfile(setup_py):
            Console.error(__name__, f'setup.py not found in {self._output_path}')
            return

        try:
            sandbox.run_setup(os.path.abspath(setup_py), [
                'sdist',
                f'--dist-dir={os.path.join(self._output_path, "setup")}',
                'bdist_wheel',
                f'--bdist-dir={os.path.join(self._output_path, "bdist")}',
                f'--dist-dir={os.path.join(self._output_path, "setup")}'
            ])
            os.remove(setup_py)
        except Exception as e:
            Console.error('Executing setup.py failed', str(e))

    def include(self, path: str):
        self._build_settings.included.append(path)

    def exclude(self, path: str):
        self._build_settings.excluded.append(path)

    def build(self):
        self._output_path = os.path.join(self._output_path, 'build')

        Console.spinner('Reading source files:', self._read_sources, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Creating internal packages:', self._create_packages, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Building application:', self._dist_files, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)

    def publish(self):
        self._output_path = os.path.join(self._output_path, 'publish')

        Console.write_line('Build:')
        Console.spinner('Reading source files:', self._read_sources, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Creating internal packages:', self._create_packages, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Building application:', self._dist_files, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)

        Console.write_line('\nPublish:')
        Console.spinner('Generating setup.py:', self._create_setup, text_foreground_color=ForegroundColorEnum.green, spinner_foreground_color=ForegroundColorEnum.blue)
        Console.write_line('Running setup.py:\n')
        self._run_setup()
        # Console.spinner('Cleaning dist path:', self._clean_dist_files)
