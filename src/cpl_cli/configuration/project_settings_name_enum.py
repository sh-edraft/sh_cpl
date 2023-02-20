from enum import Enum


class ProjectSettingsNameEnum(Enum):
    name = "Name"
    version = "Version"
    author = "Author"
    author_email = "AuthorEmail"
    description = "Description"
    long_description = "LongDescription"
    url = "URL"
    copyright_date = "CopyrightDate"
    copyright_name = "CopyrightName"
    license_name = "LicenseName"
    license_description = "LicenseDescription"
    dependencies = "Dependencies"
    dev_dependencies = "DevDependencies"
    python_version = "PythonVersion"
    python_path = "PythonPath"
    classifiers = "Classifiers"
