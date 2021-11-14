import asyncio
from cpl_core.application import ApplicationBuilder

from application import Application
from startup import Startup


async def main():
    app_builder = ApplicationBuilder(Application)
    app_builder.use_startup(Startup)
    app = await app_builder.build_async()
    await app.run_async()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
