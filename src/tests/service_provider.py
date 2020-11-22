from sh_edraft.logging.base.logger_base import LoggerBase
from sh_edraft.publish import Publisher
from sh_edraft.publish.base import PublisherBase
from sh_edraft.service.base import ServiceProviderBase


class ServiceProviderTest:

    @staticmethod
    def start(services: ServiceProviderBase):
        services.add_transient(Publisher, services.get_service(LoggerBase), '../', '../../dist', [])

        publisher: Publisher = services.get_service(PublisherBase)

        if publisher is None or publisher.source_path != '../' or publisher.dist_path != '../../dist':
            raise Exception(f'{__name__}: Invalid value in {Publisher.__name__}')

        services.remove_service(PublisherBase)
        if services.get_service(PublisherBase) is not None:
            raise Exception(f'{__name__}: Service {Publisher.__name__} was not removed')
