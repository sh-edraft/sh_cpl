from abc import abstractmethod

from cpl.dependency_injection.service_abc import ServiceABC
from cpl.mailing.email import EMail


class EMailClientABC(ServiceABC):

    @abstractmethod
    def __init__(self):
        ServiceABC.__init__(self)

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def send_mail(self, email: EMail): pass
