import os
import shutil
from string import Template as stringTemplate

from setuptools import sandbox

from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publishing.base.publisher_base import PublisherBase
from sh_edraft.publishing.model.publish_settings_model import PublishSettings
from sh_edraft.publishing.model.template import Template


class Publisher(PublisherBase):

    def __init__(self, logger: LoggerBase, publish_settings: PublishSettings):
        PublisherBase.__init__(self)

        self._logger: LoggerBase = logger
        self._publish_settings: PublishSettings = publish_settings

        self._included_files: list[str] = []

    @property
    def source_path(self) -> str:
        return self._publish_settings.source_path

    @property
    def dist_path(self):
        return self._publish_settings.dist_path

    def _get_template_output(self, t: Template, name: str, imports: str) -> str:
        self._logger.trace(__name__, f'Started {__name__}._get_template_output')
        try:
            if t.file_content == '':
                raise Exception(f'Template is empty: {t.template_path}')

            self._logger.trace(__name__, f'Stopped {__name__}._get_template_output')
            return stringTemplate(t.file_content).substitute(
                Name=name,
                Description=t.description,
                LongDescription=t.long_description,
                CopyrightDate=t.copyright_date,
                CopyrightName=t.copyright_name,
                LicenseName=t.license_name,
                LicenseDescription=t.license_description,
                Title=t.title if t.title is not None and t.title != '' else name,
                Author=t.author,
                Version=t.version.to_str(),
                Major=t.version.major,
                Minor=t.version.minor,
                Micro=t.version.micro,
                Imports=imports
            )
        except Exception as e:
            self._logger.fatal(__name__, f'Cannot read Template: {t.template_path}', e)
            self._logger.trace(__name__, f'Stopped {__name__}._get_template_output')

    def _read_source_path(self):
        self._logger.trace(__name__, f'Started {__name__}._read_source_path')
        included_files = self._publish_settings.included_files
        for included in included_files:
            if os.path.isdir(included):
                self._publish_settings.included_files.remove(included)

                for r, d, f in os.walk(included):
                    for file in f:
                        rel_path = os.path.relpath(r)
                        if not rel_path.startswith('.'):
                            rel_path = f'./{rel_path}'

                        file_path = os.path.join(self._publish_settings.source_path, r, file)
                        if os.path.isfile(file_path):
                            self._included_files.append(file_path)
                        elif os.path.isfile(os.path.join(rel_path, file)):
                            self._included_files.append(os.path.join(rel_path, file))
                        else:
                            self._logger.fatal(__name__, f'File not found: {file}')

            elif os.path.isfile(included):
                self._included_files.append(included)
            else:
                self._logger.fatal(__name__, f'File not found: {included}')

        for r, d, f in os.walk(self._publish_settings.source_path):
            for file in f:
                is_file_excluded = False
                if os.path.join(r, file) in self._publish_settings.excluded_files:
                    is_file_excluded = True
                else:
                    for excluded in self._publish_settings.excluded_files:
                        if os.path.join(r, file).__contains__(excluded):
                            is_file_excluded = True

                if not is_file_excluded and file.endswith('.py') or file in self._publish_settings.included_files:
                    self._included_files.append(os.path.join(r, file))

        self._logger.trace(__name__, f'Stopped {__name__}._read_source_path')

    def _read_templates(self):
        self._logger.trace(__name__, f'Started {__name__}._read_templates')
        for t in self._publish_settings.templates:
            output_template: str = ''
            if not os.path.isfile(t.template_path):
                self._logger.fatal(__name__, f'Template not found: {t.template_path}')

            with open(t.template_path) as template:
                t.file_content = template.read()
                template.close()
                if t.file_content == '':
                    self._logger.fatal(__name__, f'Template is empty: {t.template_path}')

        self._logger.trace(__name__, f'Stopped {__name__}._read_templates')

    def _create_dist_path(self):
        self._logger.trace(__name__, f'Started {__name__}._create_dist_path')
        if os.path.isdir(self._publish_settings.dist_path):
            try:
                shutil.rmtree(self._publish_settings.dist_path)
                self._logger.info(__name__, f'Deleted {self._publish_settings.dist_path}')
            except Exception as e:
                self._logger.fatal(__name__, f'Cannot delete old dist directory', e)

        if not os.path.isdir(self._publish_settings.dist_path):
            try:
                os.makedirs(self._publish_settings.dist_path)
                self._logger.debug(__name__, f'Created directories: {self._publish_settings.dist_path}')
                self._logger.info(__name__, f'Created dist directory')
            except Exception as e:
                self._logger.fatal(__name__, f'Cannot create dist directory', e)

        self._logger.trace(__name__, f'Stopped {__name__}._create_dist_path')

    @staticmethod
    def _get_template_name_from_dirs(file: str) -> str:
        dirs = os.path.dirname(file).split('/')
        for d in dirs:
            if d.__contains__('.'):
                dirs.remove(d)

        if len(dirs) == 0:
            return os.path.basename(file)
        else:
            return '.'.join(dirs)

    def _write_templates(self):
        self._logger.trace(__name__, f'Started {__name__}._write_templates')
        for template in self._publish_settings.templates:
            for file in self._included_files:
                if os.path.basename(file) == '__init__.py' and file not in self._publish_settings.excluded_files:
                    template_name = template.name
                    if template.name == 'all' or template.name == '':
                        template_name = self._get_template_name_from_dirs(file)
                    else:
                        name = self._get_template_name_from_dirs(file)

                        if name.__contains__('.'):
                            if template.name != name.split('.')[len(name.split('.')) - 1]:
                                continue

                        else:
                            if template.name != name:
                                continue

                    try:
                        module_file_lines: list[str] = []
                        module_py_lines: list[str] = []
                        imports = ''
                        with open(file, 'r') as py_file:
                            module_file_lines = py_file.readlines()
                            py_file.close()

                        if len(module_file_lines) == 0:
                            with open(file, 'w+') as py_file:
                                py_file.write(self._get_template_output(template, template_name, '# imports:'))
                                py_file.close()
                                self._logger.debug(__name__, f'Written to {file}')
                        else:
                            is_started = False
                            for line in module_file_lines:
                                if line.__contains__('# imports'):
                                    is_started = True

                                if (line.__contains__('from') or line.__contains__('import')) and is_started:
                                    module_py_lines.append(line.replace('\n', ''))

                            if len(module_py_lines) > 0:
                                imports = '\n'.join(module_py_lines)

                            with open(file, 'w+') as py_file:
                                py_file.write(self._get_template_output(template, template_name, imports))
                                py_file.close()
                                self._logger.debug(__name__, f'Written to {file}')

                    except Exception as e:
                        self._logger.error(__name__, f'Cannot write to file: {file}', e)

        self._logger.info(__name__, f'Written to all included modules')
        self._logger.trace(__name__, f'Stopped {__name__}._write_templates')

    def _copy_all_included_files(self):
        self._logger.trace(__name__, f'Started {__name__}._copy_all_included_files')
        dist_path = self._publish_settings.dist_path
        if self._publish_settings.dist_path.endswith('/'):
            dist_path = dist_path[:len(dist_path) - 1]

        for file in self._included_files:
            is_file_excluded = False
            if file in self._publish_settings.excluded_files:
                is_file_excluded = True
            else:
                for excluded in self._publish_settings.excluded_files:
                    if file.__contains__(excluded):
                        is_file_excluded = True

            if not is_file_excluded:
                output_file = ''

                if file.startswith('..'):
                    output_file = file.replace('..', '')
                elif file.startswith('.'):
                    output_file = file.replace('.', '', 1)

                if output_file.__contains__('..'):
                    output_file = os.path.join(dist_path, os.path.basename(file))
                else:
                    output_file = f'{dist_path}{output_file}'

                output_path = os.path.dirname(output_file)

                try:
                    if not os.path.isdir(output_path):
                        os.makedirs(output_path)
                except Exception as e:
                    self._logger.error(__name__, f'Cannot create directories: {output_path}', e)

                try:
                    shutil.copy(file, output_file)
                except Exception as e:
                    self._logger.error(__name__, f'Cannot copy file: {file} to {output_path}', e)

                self._logger.debug(__name__, f'Copied {file} to {output_path}')

        self._logger.info(__name__, f'Copied all included files')
        self._logger.trace(__name__, f'Stopped {__name__}._copy_all_included_files')

    def include(self, path: str):
        self._logger.trace(__name__, f'Started {__name__}.include')
        self._publish_settings.included_files.append(path)
        self._logger.trace(__name__, f'Stopped {__name__}.include')

    def exclude(self, path: str):
        self._logger.trace(__name__, f'Started {__name__}.exclude')
        self._publish_settings.excluded_files.append(path)
        self._logger.trace(__name__, f'Stopped {__name__}.exclude')

    def create(self):
        self._logger.trace(__name__, f'Started {__name__}.create')
        if not self._publish_settings.dist_path.endswith('/'):
            self._publish_settings.dist_path += '/'

        self._read_source_path()
        self._read_templates()
        self._create_dist_path()
        self._logger.trace(__name__, f'Stopped {__name__}.create')

    def build(self):
        self._logger.trace(__name__, f'Started {__name__}.build')
        self._write_templates()
        self._copy_all_included_files()
        self._logger.trace(__name__, f'Stopped {__name__}.build')

    def publish(self):
        self._logger.trace(__name__, f'Started {__name__}.publish')
        setup_py = os.path.join(self._publish_settings.dist_path, 'setup.py')
        if not os.path.isfile(setup_py):
            self._logger.fatal(__name__, f'setup.py not found in {self._publish_settings.dist_path}')

        sandbox.run_setup(os.path.abspath(setup_py), ['sdist', 'bdist_wheel'])
        self._logger.trace(__name__, f'Stopped {__name__}.publish')
