import os

from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publish.base import PublisherBase
from sh_edraft.service.base import ServiceProviderBase
from sh_edraft.source_code.model import Version
from sh_edraft.publish import Publisher
from sh_edraft.publish.model import Template


class PublisherTest:

    @staticmethod
    def start(services: ServiceProviderBase):
        version = Version(2020, 12, 5).to_dict()
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
                version
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
                version
            )
        ]

        source = '../'
        dist = '../../dist'

        services.add_transient(Publisher, services.get_service(LoggerBase), source, dist, templates)
        publisher: Publisher = services.get_service(PublisherBase)

        publisher.exclude('../tests/')
        publisher.include('../../LICENSE')
        publisher.include('../../README.md')

        publisher.create()
        publisher.publish()

        if not os.path.isdir(dist):
            raise Exception(f'{__name__}: Dist path was not created')
