import unittest

from cpl_core.utils import CredentialManager


class CredentialManagerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_encrypt(self):
        self.assertEqual("ZkVjSkplQUx4aW1zWHlPbA==", CredentialManager.encrypt("fEcJJeALximsXyOl"))
        self.assertEqual("QmtVd1l4dW5Sck9jRmVTQQ==", CredentialManager.encrypt("BkUwYxunRrOcFeSA"))
        self.assertEqual("c2FtaHF1VkNSdmZpSGxDcQ==", CredentialManager.encrypt("samhquVCRvfiHlCq"))
        self.assertEqual("S05aWHBPYW9DbkRSV01rWQ==", CredentialManager.encrypt("KNZXpOaoCnDRWMkY"))
        self.assertEqual("QmtUV0Zsb3h1Y254UkJWeg==", CredentialManager.encrypt("BkTWFloxucnxRBVz"))
        self.assertEqual("VFdNTkRuYXB1b1dndXNKdw==", CredentialManager.encrypt("TWMNDnapuoWgusJw"))
        self.assertEqual("WVRiQXVSZXRMblpicWNrcQ==", CredentialManager.encrypt("YTbAuRetLnZbqckq"))
        self.assertEqual("bmN4aExackxhYUVVdnV2VA==", CredentialManager.encrypt("ncxhLZrLaaEUvuvT"))
        self.assertEqual("dmpNT0J5U0lLQmFrc0pIYQ==", CredentialManager.encrypt("vjMOBySIKBaksJHa"))
        self.assertEqual("ZHd6WHFzSlFvQlhRbGtVZw==", CredentialManager.encrypt("dwzXqsJQoBXQlkUg"))
        self.assertEqual("Q0lmUUhOREtiUmxnY2VCbQ==", CredentialManager.encrypt("CIfQHNDKbRlgceBm"))

    def test_decrypt(self):
        self.assertEqual("fEcJJeALximsXyOl", CredentialManager.decrypt("ZkVjSkplQUx4aW1zWHlPbA=="))
        self.assertEqual("BkUwYxunRrOcFeSA", CredentialManager.decrypt("QmtVd1l4dW5Sck9jRmVTQQ=="))
        self.assertEqual("samhquVCRvfiHlCq", CredentialManager.decrypt("c2FtaHF1VkNSdmZpSGxDcQ=="))
        self.assertEqual("KNZXpOaoCnDRWMkY", CredentialManager.decrypt("S05aWHBPYW9DbkRSV01rWQ=="))
        self.assertEqual("BkTWFloxucnxRBVz", CredentialManager.decrypt("QmtUV0Zsb3h1Y254UkJWeg=="))
        self.assertEqual("TWMNDnapuoWgusJw", CredentialManager.decrypt("VFdNTkRuYXB1b1dndXNKdw=="))
        self.assertEqual("YTbAuRetLnZbqckq", CredentialManager.decrypt("WVRiQXVSZXRMblpicWNrcQ=="))
        self.assertEqual("ncxhLZrLaaEUvuvT", CredentialManager.decrypt("bmN4aExackxhYUVVdnV2VA=="))
        self.assertEqual("vjMOBySIKBaksJHa", CredentialManager.decrypt("dmpNT0J5U0lLQmFrc0pIYQ=="))
        self.assertEqual("dwzXqsJQoBXQlkUg", CredentialManager.decrypt("ZHd6WHFzSlFvQlhRbGtVZw=="))
        self.assertEqual("CIfQHNDKbRlgceBm", CredentialManager.decrypt("Q0lmUUhOREtiUmxnY2VCbQ=="))

    def test_build_string(self):
        self.assertEqual(
            "TestStringWithCredentialsfEcJJeALximsXyOlHere",
            CredentialManager.build_string("TestStringWithCredentials$credentialsHere", "ZkVjSkplQUx4aW1zWHlPbA=="),
        )
