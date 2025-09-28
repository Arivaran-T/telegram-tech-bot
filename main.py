import asyncio
import logging
import sys

from app.bot_app import run_the_bot


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(run_the_bot())
