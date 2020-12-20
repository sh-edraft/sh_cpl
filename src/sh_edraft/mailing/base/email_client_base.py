from abc import abstractmethod

from sh_edraft.mailing.model.email import EMail
from sh_edraft.service.base.service_base import ServiceBase


class EMailClientBase(ServiceBase):

    @abstractmethod
    def __init__(self):
        ServiceBase.__init__(self)

    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def send_mail(self, email: EMail): pass
