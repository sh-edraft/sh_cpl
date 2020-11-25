from enum import Enum


class PublishSettingsName(Enum):

    publish = 'Publish'
    source_path = 'SourcePath'
    dist_path = 'DistPath'
    templates = 'Templates'
    included_files = 'IncludedFiles'
    excluded_files = 'ExcludedFiles'
    template_ending = 'TemplateEnding'
