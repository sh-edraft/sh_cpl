import base64


class CredentialManager:
    """
    Handles credentials
    """

    @staticmethod
    def encrypt(string: str) -> str:
        """
        Encode with base64
        :param string:
        :return:
        """
        return base64.b64encode(string.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(string: str) -> str:
        """
        Decode with base64
        :param string:
        :return:
        """
        return base64.b64decode(string).decode('utf-8')

    @staticmethod
    def build_string(string: str, credentials: str):
        """
        Builds string with credentials in it
        :param string:
        :param credentials:
        :return:
        """
        return string.replace('$credentials', CredentialManager.decrypt(credentials))

