import importlib
import os
import shutil
import sys
import traceback
from importlib import util
from string import Template as stringTemplate

import setuptools
from packaging import version
from setuptools import sandbox

from cpl.console.foreground_color_enum import ForegroundColorEnum
from cpl.console.console import Console
from cpl.environment.application_environment_abc import ApplicationEnvironmentABC
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_type_enum import ProjectTypeEnum
from cpl_cli.publish.publisher_abc import PublisherABC
from cpl_cli.templates.build.init_template import InitTemplate
from cpl_cli.templates.publish.setup_template import SetupTemplate


class PublisherService(PublisherABC):

    def __init__(self, env: ApplicationEnvironmentABC, project: ProjectSettings, build: BuildSettings):
        """
        Service to build or publish files for distribution
        :param env:
        :param project:
        :param build:
        """
        PublisherABC.__init__(self)

        self._env = env
        self._project_settings = project
        self._build_settings = build

        self._source_path = os.path.join(self._env.working_directory, self._build_settings.source_path)
        self._output_path = os.path.join(self._env.working_directory, self._build_settings.output_path)

        self._included_files: list[str] = []
        self._included_dirs: list[str] = []
        self._distributed_files: list[str] = []

    @property
    def source_path(self) -> str:
        return self._source_path

    @property
    def dist_path(self) -> str:
        return self._output_path

    @staticmethod
    def _get_module_name_from_dirs(file: str) -> str:
        """
        Extracts module name from directories
        :param file:
        :return:
        """
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
        """
        Deletes full path tree
        :param path:
        :return:
        """
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
            except Exception as e:
                Console.error(f'{e}')
                exit()

    @staticmethod
    def _create_path(path: str):
        """
        Creates full path tree
        :param path:
        :return:
        """
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except Exception as e:
                Console.error(f'{e}')
                exit()

    def _is_path_included(self, path: str) -> bool:
        """
        Checks if the path is included
        :param path:
        :return:
        """
        for included in self._build_settings.included:
            if included.startswith('*'):
                included = included.replace('*', '')

            if included in path and path not in self._build_settings.excluded:
                return True

        return False

    def _is_path_excluded(self, path: str) -> bool:
        """
        Checks if the path is excluded
        :param path:
        :return:
        """
        for excluded in self._build_settings.excluded:
            if excluded.startswith('*'):
                excluded = excluded.replace('*', '')

            if excluded in path and not self._is_path_included(path):
                return True

        return False

    def _read_sources(self):
        """
        Reads all source files and save included files
        :return:
        """
        for file in self._build_settings.included:
            rel_path = os.path.relpath(file)
            if os.path.isdir(rel_path):
                for r, d, f in os.walk(rel_path):
                    for sub_file in f:
                        relative_path = os.path.relpath(r)
                        file_path = os.path.join(relative_path, os.path.relpath(sub_file))

                        print(file_path)
                        self._included_files.append(os.path.relpath(file_path))

            elif os.path.isfile(rel_path):
                print(rel_path)
                self._included_files.append(rel_path)

        for r, d, f in os.walk(self._build_settings.source_path):
            for file in f:
                relative_path = os.path.relpath(r)
                file_path = os.path.join(relative_path, os.path.relpath(file))
                if self._is_path_excluded(relative_path):
                    break

                if len(d) > 0:
                    for directory in d:
                        empty_dir = os.path.join(os.path.dirname(file_path), directory)
                        if len(os.listdir(empty_dir)) == 0:
                            self._included_dirs.append(empty_dir)

                if not self._is_path_excluded(relative_path):
                    self._included_files.append(os.path.relpath(file_path))

    def _create_packages(self):
        """
        Writes information from template to all included __init__.py
        :return:
        """
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
        """
        Copies all included source files to dist_path
        :return:
        """
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
        """
        Deletes all included source files from dist_path
        :return:
        """
        paths: list[str] = []
        for file in self._distributed_files:
            paths.append(os.path.dirname(file))

            if os.path.isfile(file):
                os.remove(file)

        for path in paths:
            if path != self._output_path and os.path.isdir(path):
                shutil.rmtree(path)

    def _create_setup(self):
        """
        Generates setup.py

        Dependencies: ProjectSettings, BuildSettings
        :return:
        """
        setup_file = os.path.join(self._output_path, 'setup.py')
        if os.path.isfile(setup_file):
            os.remove(setup_file)

        main = None
        try:
            main_name = ''

            if '.' in self._build_settings.main:
                length = len(self._build_settings.main.split('.'))
                main_name = self._build_settings.main.split('.')[length-1]

            sys.path.insert(0, self._source_path)
            main_mod = __import__(self._build_settings.main)
            main = getattr(main_mod, main_name)
        except Exception as e:
            Console.error('Could not find entry point', str(e))
            return

        if main is None or not callable(main) and not hasattr(main, 'main'):
            Console.error('Could not find entry point')
            return

        if callable(main):
            mod_name = main.__module__
            func_name = main.__name__
        else:
            mod_name = main.__name__
            func_name = main.main.__name__

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
                        f'{self._build_settings.entry_point} = {mod_name}:{func_name}'
                    ]
                },
                PackageData=self._build_settings.package_data
            )
            setup_py.write(setup_string)
            setup_py.close()

    def _run_setup(self):
        """
        Starts setup.py
        :return:
        """
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
        """
        Includes given path from sources
        :param path:
        :return:
        """
        self._build_settings.included.append(path)

    def exclude(self, path: str):
        """
        Excludes given path from sources
        :param path:
        :return:
        """
        self._build_settings.excluded.append(path)

    def build(self):
        """
        Build the CPL project to dist_path/build

        1. Reads all included source files
        2. Writes informations from template to all included __init__.py
        3. Copies all included source files to dist_path/build
        :return:
        """
        self._output_path = os.path.join(self._output_path, 'build')

        Console.spinner('Reading source files:', self._read_sources, text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Creating internal packages:', self._create_packages,
                        text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Building application:', self._dist_files, text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)

    def publish(self):
        """
        Publishes the CPL project to dist_path/publish

        1. Builds the project
        2. Generates setup.py
        3. Start setup.py
        4. Remove all included source from dist_path/publish
        :return:
        """
        if self._build_settings.project_type != ProjectTypeEnum.library.value:
            Console.error(f'Project must be a {ProjectTypeEnum.library.value} for publishing.')
            return

        self._output_path = os.path.join(self._output_path, 'publish')

        Console.write_line('Build:')
        Console.spinner('Reading source files:', self._read_sources, text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Creating internal packages:', self._create_packages,
                        text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)
        Console.spinner('Building application:', self._dist_files, text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)

        Console.write_line('\nPublish:')
        Console.spinner('Generating setup.py:', self._create_setup, text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)
        Console.write_line('Running setup.py:\n')
        self._run_setup()
        Console.spinner('Cleaning dist path:', self._clean_dist_files, text_foreground_color=ForegroundColorEnum.green,
                        spinner_foreground_color=ForegroundColorEnum.blue)
