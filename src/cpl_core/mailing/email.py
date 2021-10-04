import re


class EMail:
    r"""Represents an email

    Parameter
    ---------
        header: list[:class:`str`]
            Header of the E-Mail
        subject: :class:`str`
            Subject of the E-Mail
        body: :class:`str`
            Body of the E-Mail
        transceiver: :class:`str`
            Transceiver of the E-Mail
        receiver: list[:class:`str`]
            Receiver of the E-Mail
    """

    def __init__(self, header: list[str] = None, subject: str = None, body: str = None, transceiver: str = None,
                 receiver: list[str] = None):
        self._header: list[str] = header

        self._subject: str = subject
        self._body: str = body

        self._transceiver: str = transceiver
        self._receiver: list[str] = receiver

    @property
    def header(self) -> str:
        return '\r\n'.join(self._header)

    @property
    def header_list(self) -> list[str]:
        return self._header

    @header.setter
    def header(self, header: list[str]):
        self._header = header

    @property
    def subject(self) -> str:
        return self._subject

    @subject.setter
    def subject(self, subject: str):
        self._subject = subject

    @property
    def body(self) -> str:
        return self._body

    @body.setter
    def body(self, body: str):
        self._body = body

    @property
    def transceiver(self) -> str:
        return self._transceiver

    @transceiver.setter
    def transceiver(self, transceiver: str):
        if self.check_mail(transceiver):
            self._transceiver = transceiver
        else:
            raise Exception(f'Invalid email: {transceiver}')

    @property
    def receiver(self) -> str:
        return ','.join(self._receiver)

    @property
    def receiver_list(self) -> list[str]:
        return self._receiver

    @receiver.setter
    def receiver(self, receiver: list[str]):
        self._receiver = receiver

    @staticmethod
    def check_mail(address: str) -> bool:
        r"""Checks if an email is valid

        Parameter
        ---------
            address: :class:`str`
                The address to check

        Returns
        -------
            Result if E-Mail is valid or not
        """
        return bool(re.search('^\\w+([.-]?\\w+)*@\\w+([.-]?\\w+)*(.\\w{2,3})+$', address))

    def add_header(self, header: str):
        r"""Adds header

        Parameter
        ---------
            header: :class:`str`
                The header of the E-Mail
        """
        if self._header is None:
            self._header = []

        self._header.append(header)

    def add_receiver(self, receiver: str):
        r"""Adds receiver

        Parameter
        ---------
            receiver: :class:`str`
                The receiver of the E-Mail
        """
        if self._receiver is None:
            self._receiver = []

        if self.check_mail(receiver):
            self._receiver.append(receiver)
        else:
            raise Exception(f'Invalid email: {receiver}')

    def get_content(self, transceiver: str):
        r"""Returns the mail as string

        Parameter
        ---------
            transceiver: :class:`str`
                The transceiver of the E-Mail

        Returns
        -------
            E-Mail as string
        """
        return str(
            f'From: {transceiver}\r\nTo: {self.receiver}\r\n{self.header}\r\nSubject: {self.subject}\r\n{self.body}').encode(
            'utf-8')
