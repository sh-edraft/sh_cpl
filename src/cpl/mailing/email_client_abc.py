from abc import abstractmethod, ABC

from cpl.mailing.email import EMail


class EMailClientABC(ABC):

    @abstractmethod
    def __init__(self):
        """
        ABC to send emails
        """
        ABC.__init__(self)

    @abstractmethod
    def connect(self):
        """
        Connects to server
        :return:
        """
        pass

    @abstractmethod
    def send_mail(self, email: EMail):
        """
        Sends email
        :param email:
        :return:
        """
        pass
