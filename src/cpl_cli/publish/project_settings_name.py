from enum import Enum


class ProjectSettingsName(Enum):

    project = 'Project'
    name = 'Name'
    author = 'Author'
    description = 'Description'
    long_description = 'LongDescription'
    copyright_date = 'CopyrightDate'
    copyright_name = 'CopyrightName'
    license_name = 'LicenseName'
    license_description = 'LicenseDescription'
    version = 'Version'
    source_path = 'SourcePath'
    dist_path = 'DistPath'
    included = 'Included'
    excluded = 'Excluded'
