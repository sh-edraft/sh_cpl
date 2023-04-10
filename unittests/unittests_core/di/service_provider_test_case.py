import unittest

from cpl_core.configuration import Configuration
from cpl_core.dependency_injection import ServiceCollection, ServiceProviderABC


class ServiceCount:
    def __init__(self):
        self.count = 0


class TestService:
    def __init__(self, count: ServiceCount):
        count.count += 1
        self.id = count.count


class DifferentService:
    def __init__(self, count: ServiceCount):
        count.count += 1
        self.id = count.count


class MoreDifferentService:
    def __init__(self, count: ServiceCount):
        count.count += 1
        self.id = count.count


class ServiceProviderTestCase(unittest.TestCase):
    def setUp(self):
        self._services = (
            ServiceCollection(Configuration())
            .add_singleton(ServiceCount)
            .add_singleton(TestService)
            .add_singleton(TestService)
            .add_transient(DifferentService)
            .add_scoped(MoreDifferentService)
            .build_service_provider()
        )

        count = self._services.get_service(ServiceCount)

    def test_get_singleton(self):
        x = self._services.get_service(TestService)
        self.assertIsNotNone(x)
        self.assertEqual(1, x.id)
        self.assertEqual(x, self._services.get_service(TestService))
        self.assertEqual(x, self._services.get_service(TestService))
        self.assertEqual(x, self._services.get_service(TestService))

    def test_get_singletons(self):
        x = self._services.get_services(list[TestService])
        self.assertEqual(2, len(x))
        self.assertEqual(1, x[0].id)
        self.assertEqual(2, x[1].id)
        self.assertNotEqual(x[0], x[1])

    def test_get_transient(self):
        x = self._services.get_service(DifferentService)
        self.assertIsNotNone(x)
        self.assertEqual(1, x.id)
        self.assertNotEqual(x, self._services.get_service(DifferentService))
        self.assertNotEqual(x, self._services.get_service(DifferentService))
        self.assertNotEqual(x, self._services.get_service(DifferentService))

    def test_scoped(self):
        scoped_id = 0
        singleton = self._services.get_service(TestService)
        with self._services.create_scope() as scope:
            sp: ServiceProviderABC = scope.service_provider
            y = sp.get_service(DifferentService)
            self.assertIsNotNone(y)
            self.assertEqual(2, y.id)
            x = sp.get_service(MoreDifferentService)
            self.assertIsNotNone(x)
            self.assertEqual(3, x.id)
            scoped_id = 3
            self.assertEqual(x.id, sp.get_service(MoreDifferentService).id)
            self.assertEqual(x.id, sp.get_service(MoreDifferentService).id)
            self.assertNotEqual(x, self._services.get_service(MoreDifferentService))
            self.assertEqual(singleton, self._services.get_service(TestService))

        self.assertIsNone(scope.service_provider)
        self.assertNotEqual(scoped_id, self._services.get_service(MoreDifferentService).id)
