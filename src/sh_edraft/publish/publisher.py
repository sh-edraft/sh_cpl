import os
import shutil
from string import Template as stringTemplate

from sh_edraft.publish.base.publisher_base import PublisherBase
from sh_edraft.publish.model.template import Template


class Publisher(PublisherBase):

    def __init__(self, source_path: str, dist_path: str, settings: list[Template]):
        super().__init__(source_path, dist_path, settings)

        self._included_files: list[str] = []
        self._excluded_files: list[str] = []

        self._template_ending = '_template.txt'

    @property
    def source_path(self) -> str:
        return self._source_path

    @property
    def dist_path(self):
        return self._dist_path

    def _get_template_output(self, t: Template, name: str, imports: str) -> str:
        try:
            if t.file_content == '':
                raise Exception(f'Template is empty: {t.template_path}')

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
            print(1, e)
            # todo: better logging

    def _read_source_path(self):
        for r, d, f in os.walk(self._source_path):
            for file in f:
                if file.endswith('.py') or file in self._included_files:
                    self._included_files.append(os.path.join(r, file))

    def _read_templates(self):
        for t in self._settings:
            output_template: str = ''
            if not os.path.isfile(t.template_path):
                raise Exception(f'Template not found: {t.template_path}')

            with open(t.template_path) as template:
                t.file_content = template.read()
                template.close()
                if t.file_content == '':
                    raise Exception(f'Template is empty: {t.template_path}')

    def _create_dist_path(self):
        if os.path.isdir(self._dist_path):
            try:
                shutil.rmtree(self._dist_path)
                print(f'Deleted {self._dist_path}')
                # todo: better logging
            except Exception as e:
                print(e)
                # todo: log error

        if not os.path.isdir(self._dist_path):
            try:
                os.makedirs(self._dist_path)
            except Exception as e:
                print(e)
                # todo: log error

    def _get_template_name_from_dirs(self, file: str) -> str:
        dirs = os.path.dirname(file).split('/')
        for d in dirs:
            if d.__contains__('.'):
                dirs.remove(d)

        if len(dirs) == 0:
            return os.path.basename(file)
        else:
            return '.'.join(dirs)

    def _write_templates(self):
        for template in self._settings:
            for file in self._included_files:
                if os.path.basename(file) == '__init__.py' and file not in self._excluded_files:
                    template_name = template.name
                    if template.name == '*' or template.name == '':
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
                                print(f'Written to {file}')
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
                                print(f'Written to {file}')

                    except Exception as e:
                        print(e)
                        # todo: better logging

    def _copy_all_included_files(self):
        dist_path = self._dist_path
        if self._dist_path.endswith('/'):
            dist_path = dist_path[:len(dist_path) - 1]

            for file in self._included_files:
                is_file_excluded = False
                if file in self._excluded_files:
                    is_file_excluded = True
                else:
                    for excluded in self._excluded_files:
                        if file.__contains__(excluded):
                            is_file_excluded = True

                if not is_file_excluded:
                    output_file = ''
                    if file.startswith('..'):
                        output_file = file.replace('..', '')

                    elif file.startswith('.'):
                        output_file = file.replace('.', '', 1)

                    output_file = f'{dist_path}{output_file}'
                    output_path = os.path.dirname(output_file)

                    try:
                        if not os.path.isdir(output_path):
                            os.makedirs(output_path)
                    except Exception as e:
                        print(e)
                        # todo: better logging

                    try:
                        shutil.copy(file, output_file)
                    except Exception as e:
                        print(e)
                        # todo: better logging

                    print(f'Copied {file} to {output_path}')
                    # todo: better logging

    def include(self, path: str):
        self._included_files.append(path)

    def exclude(self, path: str):
        self._excluded_files.append(path)

    def create(self):
        if not self._dist_path.endswith('/'):
            self._dist_path += '/'

        self._read_source_path()
        self._read_templates()
        self._create_dist_path()

    def publish(self):
        self._write_templates()
        self._copy_all_included_files()
