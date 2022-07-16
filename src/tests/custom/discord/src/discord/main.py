import asyncio

from cpl_core.application import ApplicationBuilder

from discord.application import Application
from discord.startup import Startup


async def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app: Application = await app_builder.build_async()
    await app.run_async()


if __name__ == '__main__':
    asyncio.run(main())
