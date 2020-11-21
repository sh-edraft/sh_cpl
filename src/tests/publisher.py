from sh_edraft.source_code.model import Version
from sh_edraft.publish import Publisher
from sh_edraft.publish.model import Template

if __name__ == '__main__':
    templates = [
        Template(
            '../../publish_templates/*_template.txt',
            '*',
            '',
            '',
            '2020',
            'sh-edraft.de',
            'MIT',
            ', see LICENSE for more details.',
            '',
            'Sven Heidemann',
            Version(2020, 12, 0.1).to_dict()
        ),
        Template(
            '../../publish_templates/*_template.txt',
            'sh_edraft',
            'common python library',
            'Library to share common classes and models used at sh-edraft.de',
            '2020',
            'sh-edraft.de',
            'MIT',
            ', see LICENSE for more details.',
            '',
            'Sven Heidemann',
            Version(2020, 12, 0.1).to_dict()
        )
    ]

    publisher = Publisher('../', '../../dist', templates)

    publisher.exclude('../tests/')
    publisher.include('../../LICENSE')
    publisher.include('../../README.md')

    publisher.create()
    publisher.publish()
