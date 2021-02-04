import base64


class CredentialManager:

    @staticmethod
    def encrypt(string: str) -> str:
        return base64.b64encode(string.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(string: str) -> str:
        return base64.b64decode(string).decode('utf-8')

    @staticmethod
    def build_string(string: str, credentials: str):
        return string.replace('$credentials', CredentialManager.decrypt(credentials))

