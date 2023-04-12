import unittest
from unittest.mock import Mock

from cpl_core.configuration import Configuration
from cpl_core.dependency_injection import ServiceCollection, ServiceLifetimeEnum, ServiceProviderABC


class ServiceCollectionTestCase(unittest.TestCase):
    def setUp(self):
        self._sc = ServiceCollection(Configuration())

    def test_add_singleton_type(self):
        self._sc.add_singleton(Mock)

        service = self._sc._service_descriptors[0]
        self.assertEqual(ServiceLifetimeEnum.singleton, service.lifetime)
        self.assertEqual(Mock, service.service_type)
        self.assertEqual(Mock, service.base_type)
        self.assertIsNone(service.implementation)

    def test_add_singleton_instance(self):
        mock = Mock()
        self._sc.add_singleton(mock)

        service = self._sc._service_descriptors[0]
        self.assertEqual(ServiceLifetimeEnum.singleton, service.lifetime)
        self.assertEqual(type(mock), service.service_type)
        self.assertEqual(type(mock), service.base_type)
        self.assertIsNotNone(service.implementation)

    def test_add_transient_type(self):
        self._sc.add_transient(Mock)

        service = self._sc._service_descriptors[0]
        self.assertEqual(ServiceLifetimeEnum.transient, service.lifetime)
        self.assertEqual(Mock, service.service_type)
        self.assertEqual(Mock, service.base_type)
        self.assertIsNone(service.implementation)

    def test_add_scoped_type(self):
        self._sc.add_scoped(Mock)

        service = self._sc._service_descriptors[0]
        self.assertEqual(ServiceLifetimeEnum.scoped, service.lifetime)
        self.assertEqual(Mock, service.service_type)
        self.assertEqual(Mock, service.base_type)
        self.assertIsNone(service.implementation)

    def test_build_service_provider(self):
        self._sc.add_singleton(Mock)
        service = self._sc._service_descriptors[0]
        self.assertIsNone(service.implementation)
        sp = self._sc.build_service_provider()
        self.assertTrue(isinstance(sp, ServiceProviderABC))
        self.assertTrue(isinstance(sp.get_service(Mock), Mock))
        self.assertIsNotNone(service.implementation)
