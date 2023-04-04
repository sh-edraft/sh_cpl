from cpl_cli.configuration.version_settings_name_enum import VersionSettingsNameEnum
from cpl_cli.configuration.build_settings import BuildSettings
from cpl_cli.configuration.build_settings_name_enum import BuildSettingsNameEnum
from cpl_cli.configuration.project_settings import ProjectSettings
from cpl_cli.configuration.project_settings_name_enum import ProjectSettingsNameEnum


class SettingsHelper:
    @staticmethod
    def get_project_settings_dict(project: ProjectSettings) -> dict:
        return {
            ProjectSettingsNameEnum.name.value: project.name,
            ProjectSettingsNameEnum.version.value: {
                VersionSettingsNameEnum.major.value: project.version.major,
                VersionSettingsNameEnum.minor.value: project.version.minor,
                VersionSettingsNameEnum.micro.value: project.version.micro,
            },
            ProjectSettingsNameEnum.author.value: project.author,
            ProjectSettingsNameEnum.author_email.value: project.author_email,
            ProjectSettingsNameEnum.description.value: project.description,
            ProjectSettingsNameEnum.long_description.value: project.long_description,
            ProjectSettingsNameEnum.url.value: project.url,
            ProjectSettingsNameEnum.copyright_date.value: project.copyright_date,
            ProjectSettingsNameEnum.copyright_name.value: project.copyright_name,
            ProjectSettingsNameEnum.license_name.value: project.license_name,
            ProjectSettingsNameEnum.license_description.value: project.license_description,
            ProjectSettingsNameEnum.dependencies.value: project.dependencies,
            ProjectSettingsNameEnum.dev_dependencies.value: project.dev_dependencies,
            ProjectSettingsNameEnum.python_version.value: project.python_version,
            ProjectSettingsNameEnum.python_path.value: project.python_path,
            ProjectSettingsNameEnum.classifiers.value: project.classifiers,
        }

    @staticmethod
    def get_build_settings_dict(build: BuildSettings) -> dict:
        return {
            BuildSettingsNameEnum.project_type.value: build.project_type,
            BuildSettingsNameEnum.source_path.value: build.source_path,
            BuildSettingsNameEnum.output_path.value: build.output_path,
            BuildSettingsNameEnum.main.value: build.main,
            BuildSettingsNameEnum.entry_point.value: build.entry_point,
            BuildSettingsNameEnum.include_package_data.value: build.include_package_data,
            BuildSettingsNameEnum.included.value: build.included,
            BuildSettingsNameEnum.excluded.value: build.excluded,
            BuildSettingsNameEnum.package_data.value: build.package_data,
            BuildSettingsNameEnum.project_references.value: build.project_references,
        }
