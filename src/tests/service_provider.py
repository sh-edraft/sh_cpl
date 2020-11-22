from sh_edraft.publish import Publisher
from sh_edraft.publish.base import PublisherBase
from sh_edraft.service.base import ServiceProviderBase


class ServiceProviderTest:

    @staticmethod
    def start(provider: ServiceProviderBase):
        provider.create()

        provider.add_transient(Publisher, None, '../', '../../dist', [])

        publisher: Publisher = provider.get_service(PublisherBase)

        if publisher is None or publisher.source_path != '../' or publisher.dist_path != '../../dist':
            raise Exception(f'{__name__}: Invalid value in {Publisher.__name__}')

        provider.remove_service(PublisherBase)
        if provider.get_service(PublisherBase) is not None:
            raise Exception(f'{__name__}: Service {Publisher.__name__} was not removed')
