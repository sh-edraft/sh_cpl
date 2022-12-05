from abc import ABC, abstractmethod

from cpl_cli.abc.file_template_abc import FileTemplateABC
from cpl_core.utils import String


class CodeFileTemplateABC(FileTemplateABC):

    @abstractmethod
    def __init__(
            self,
            name: str,
            path: str,
            code: str,
            use_application_api: bool,
            use_startup: bool,
            use_service_providing: bool,
            use_async: bool,
    ):
        FileTemplateABC.__init__(self, name, path, code)
        self._use_application_api = use_application_api
        self._use_startup = use_startup
        self._use_service_providing = use_service_providing
        self._use_async = use_async
