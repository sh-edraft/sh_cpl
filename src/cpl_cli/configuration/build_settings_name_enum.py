from enum import Enum


class BuildSettingsNameEnum(Enum):

    source_path = 'SourcePath'
    output_path = 'OutputPath'
    main = 'Main'
    entry_point = 'EntryPoint'
    include_package_data = 'IncludePackageData'
    included = 'Included'
    excluded = 'Excluded'
    package_data = 'PackageData'
