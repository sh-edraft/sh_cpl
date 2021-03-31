import os

from cpl_cli.templates.template_file_abc import TemplateFileABC


class TemplateBuilder:

    @staticmethod
    def build(project_path: str, template: TemplateFileABC):
        """
        Creates template
        :param project_path:
        :param template:
        :return:
        """
        file_path = os.path.join(project_path, template.path, template.name)
        file_rel_path = os.path.join(project_path, template.path)

        if not os.path.isdir(file_rel_path):
            os.makedirs(file_rel_path)

        with open(file_path, 'w') as license_file:
            license_file.write(template.value)
            license_file.close()
