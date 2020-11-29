from typing import Optional

from sh_edraft.coding.model.version import Version
from sh_edraft.configuration.base.configuration_model_base import ConfigurationModelBase
from sh_edraft.publishing.model.template_enum import TemplateEnum


class Template(ConfigurationModelBase):

    def __init__(
            self,
            template_path: Optional[str] = None,
            name: Optional[str] = None,
            description: Optional[str] = None,
            long_description: Optional[str] = None,
            copyright_date: Optional[str] = None,
            copyright_name: Optional[str] = None,
            license_name: Optional[str] = None,
            license_description: Optional[str] = None,
            title: Optional[str] = None,
            author: Optional[str] = None,
            version: Optional[dict] = None
    ):
        ConfigurationModelBase.__init__(self)
        self._template_path: Optional[str] = template_path
        self._name: Optional[str] = name
        self._description: Optional[str] = description
        self._long_description: Optional[str] = long_description
        self._copyright_date: Optional[str] = copyright_date
        self._copyright_name: Optional[str] = copyright_name
        self._license_name: Optional[str] = license_name
        self._license_description: Optional[str] = license_description
        self._title: Optional[str] = title
        self._author: Optional[str] = author

        self._version: Optional[Version] = Version()
        self._version.from_dict(version)
        
        self._file_content: Optional[str] = None

    @property
    def template_path(self) -> Optional[str]:
        return self._template_path

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def long_description(self) -> Optional[str]:
        return self._long_description

    @property
    def copyright_date(self) -> Optional[str]:
        return self._copyright_date

    @property
    def copyright_name(self) -> Optional[str]:
        return self._copyright_name

    @property
    def license_name(self) -> Optional[str]:
        return self._license_name

    @property
    def license_description(self) -> Optional[str]:
        return self._license_description

    @property
    def title(self) -> Optional[str]:
        return self._title

    @property
    def author(self) -> Optional[str]:
        return self._author

    @property
    def version(self) -> Optional[Version]:
        return self._version
    
    @property
    def file_content(self) -> Optional[str]:
        return self._file_content
    
    @file_content.setter
    def file_content(self, file_content: Optional[str]):
        self._file_content = file_content

    def from_dict(self, settings: dict):
        self._template_path = settings[TemplateEnum.TemplatePath.value]
        self._name = settings[TemplateEnum.Name.value]
        self._description = settings[TemplateEnum.Description.value]
        self._long_description = settings[TemplateEnum.LongDescription.value]
        self._copyright_date = settings[TemplateEnum.CopyrightDate.value]
        self._copyright_name = settings[TemplateEnum.CopyrightName.value]
        self._license_name = settings[TemplateEnum.LicenseName.value]
        self._license_description = settings[TemplateEnum.LicenseDescription.value]
        self._title = settings[TemplateEnum.Title.value]
        self._author = settings[TemplateEnum.Author.value]
        self._version.from_dict(settings[TemplateEnum.Version.value])

    def to_dict(self) -> dict:
        version: Optional[dict] = None
        if self._version is not None:
            version = self._version.to_dict()

        return {
            TemplateEnum.TemplatePath.value: self._template_path,
            TemplateEnum.Name.value: self._name,
            TemplateEnum.Description.value: self._description,
            TemplateEnum.LongDescription.value: self._long_description,
            TemplateEnum.CopyrightDate.value: self._copyright_date,
            TemplateEnum.CopyrightName.value: self._copyright_name,
            TemplateEnum.LicenseName.value: self._license_name,
            TemplateEnum.LicenseDescription.value: self._license_description,
            TemplateEnum.Title.value: self._title,
            TemplateEnum.Author.value: self._author,
            TemplateEnum.Version.value: version
        }
