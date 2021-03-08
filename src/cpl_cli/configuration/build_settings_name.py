from enum import Enum


class BuildSettingsName(Enum):

    sourcePath = 'SourcePath'
    outputPath = 'OutputPath'
    main = 'Main'
    entry_point = 'EntryPoint'
    include_package_data = 'IncludePackageData'
    included = 'Included'
    excluded = 'Excluded'
