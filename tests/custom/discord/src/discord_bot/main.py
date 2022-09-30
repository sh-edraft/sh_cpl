import asyncio
from typing import Optional

from cpl_core.application import ApplicationBuilder, ApplicationABC

from discord_bot.application import Application
from discord_bot.startup import Startup


class Main:

    def __init__(self):
        self._app: Optional[Application] = None

    async def main(self):
        app_builder = ApplicationBuilder(Application)
        app_builder.use_startup(Startup)
        self._app: ApplicationABC = await app_builder.build_async()
        await self._app.run_async()

    async def stop(self):
        await self._app.stop_async()


if __name__ == '__main__':
    main = Main()
    try:
        asyncio.run(main.main())
    except KeyboardInterrupt:
        asyncio.run(main.stop())
