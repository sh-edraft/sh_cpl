from enum import Enum


class BuildSettingsName(Enum):

    sourcePath = 'sourcePath'
    outputPath = 'outputPath'
    main = 'main'
    entry_point = 'entryPoint'
    include_package_data = 'includePackageData'
    included = 'included'
    excluded = 'excluded'
