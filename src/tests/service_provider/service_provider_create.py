import unittest

from sh_edraft.service import ServiceProvider


class ServiceProviderCreate(unittest.TestCase):

    def test_create(self):
        provider = ServiceProvider()
        self.assertIsNotNone(provider)
        provider.init(())
        provider.create()
        self.assertIsNotNone(provider)
