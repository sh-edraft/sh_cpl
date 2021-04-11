from enum import Enum


class BuildSettingsNameEnum(Enum):

    project_type = 'ProjectType'
    source_path = 'SourcePath'
    output_path = 'OutputPath'
    main = 'Main'
    entry_point = 'EntryPoint'
    include_package_data = 'IncludePackageData'
    included = 'Included'
    excluded = 'Excluded'
    package_data = 'PackageData'
    project_references = 'ProjectReferences'
