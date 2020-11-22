from sh_edraft.publish import Publisher
from sh_edraft.service import ServiceProvider


class ServiceProviderTest:

    @staticmethod
    def start() -> ServiceProvider:
        provider = ServiceProvider()
        provider.create()

        provider.add_transient(Publisher, None, '../', '../../dist', [])

        publisher: Publisher = provider.get_service(Publisher)

        if publisher.source_path != '../' or publisher.dist_path != '../../dist':
            raise Exception(f'{__name__}: Invalid value in {Publisher.__name__}')

        provider.remove_service(Publisher)
        if provider.get_service(Publisher) is not None:
            raise Exception(f'{__name__}: Service {Publisher.__name__} was not removed')

        return provider
