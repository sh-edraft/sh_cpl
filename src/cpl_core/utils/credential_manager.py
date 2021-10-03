import base64


class CredentialManager:
    r"""Handles credential encryption and decryption"""

    @staticmethod
    def encrypt(string: str) -> str:
        r"""Encode with base64

        Parameter
        ---------
            string: :class:`str`
                String to encode

        Returns
        -------
            Encoded string
        """
        return base64.b64encode(string.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(string: str) -> str:
        r"""Decode with base64

        Parameter
        ---------
            string: :class:`str`
                String to decode

        Returns
        -------
            Decoded string
        """
        return base64.b64decode(string).decode('utf-8')

    @staticmethod
    def build_string(string: str, credentials: str):
        r"""Builds string with credentials in it

        Parameter
        ---------
            string: :class:`str`
                String in which the variable is replaced by credentials
            credentials: :class:`str`
                String to encode

        Returns
        -------
            Decoded string
        """
        return string.replace('$credentials', CredentialManager.decrypt(credentials))

