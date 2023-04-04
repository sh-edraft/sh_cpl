import os

from cpl_cli.abc.project_type_abc import ProjectTypeABC
from cpl_cli.configuration import WorkspaceSettings
from cpl_core.utils import String


class DiscordBot(ProjectTypeABC):
    def __init__(
        self,
        base_path: str,
        project_name: str,
        workspace: WorkspaceSettings,
        use_application_api: bool,
        use_startup: bool,
        use_service_providing: bool,
        use_async: bool,
        project_file_data: dict,
    ):
        from project_file_discord import DiscordBotProjectFile
        from project_file_discord_appsettings import DiscordBotProjectFileAppsettings
        from project_file_discord_code_application import DiscordBotProjectFileApplication
        from project_file_discord_code_main import DiscordBotProjectFileMain
        from project_file_discord_code_startup import DiscordBotProjectFileStartup
        from project_file_discord_readme import DiscordBotProjectFileReadme
        from project_file_discord_license import DiscordBotProjectFileLicense
        from schematic_discord_init import DiscordBotInit
        from schematic_discord_event import Event
        from schematic_discord_command import Command

        use_application_api, use_startup, use_service_providing, use_async = True, True, True, True

        ProjectTypeABC.__init__(
            self,
            base_path,
            project_name,
            workspace,
            use_application_api,
            use_startup,
            use_service_providing,
            use_async,
            project_file_data,
        )

        project_path = f'{base_path}{String.convert_to_snake_case(project_name.split("/")[-1])}/'

        self.add_template(DiscordBotProjectFile(project_name.split("/")[-1], project_path, project_file_data))
        if workspace is None:
            self.add_template(DiscordBotProjectFileLicense(""))
            self.add_template(DiscordBotProjectFileReadme(""))
            self.add_template(DiscordBotInit("", "init", f"{base_path}tests/"))

        self.add_template(DiscordBotInit("", "init", project_path))
        self.add_template(DiscordBotProjectFileAppsettings(project_path))

        self.add_template(DiscordBotInit("", "init", f"{project_path}events/"))
        self.add_template(Event("OnReady", "event", f"{project_path}events/"))
        self.add_template(DiscordBotInit("", "init", f"{project_path}commands/"))
        self.add_template(Command("Ping", "command", f"{project_path}commands/"))

        self.add_template(
            DiscordBotProjectFileApplication(
                project_path, use_application_api, use_startup, use_service_providing, use_async
            )
        )
        self.add_template(
            DiscordBotProjectFileStartup(
                project_name.split("/")[-1],
                project_path,
                use_application_api,
                use_startup,
                use_service_providing,
                use_async,
            )
        )
        self.add_template(
            DiscordBotProjectFileMain(
                project_name.split("/")[-1],
                project_path,
                use_application_api,
                use_startup,
                use_service_providing,
                use_async,
            )
        )
