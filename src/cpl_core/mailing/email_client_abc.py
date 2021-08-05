from abc import abstractmethod, ABC

from cpl_core.mailing.email import EMail


class EMailClientABC(ABC):
    """ABC of :class:`cpl.mailing.email_client_service.EMailClient`"""

    @abstractmethod
    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def connect(self):
        r"""Connects to server"""
        pass

    @abstractmethod
    def send_mail(self, email: EMail):
        r"""Sends email

        Parameter
        ---------
            email: :class:`cpl.mailing.email.EMail`
                Object of the E-Mail to send
        """
        pass
