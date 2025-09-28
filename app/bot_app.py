import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.database import async_engine
from app.command_handlers import start, account, manage_users


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def run_the_bot() -> None:
    try:
        # Initialize Bot instance
        print(f"Initialize Bot instance...")
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        dp = Dispatcher()

        # Initialize the database
        print(f"Initializing the database...")
        await init_db()

        # Set bot commands shown in the Telegram UI
        commands = [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="account", description="View account details"),
        ]

        await bot.set_my_commands(commands)

        dp.include_router(start.router)
        dp.include_router(account.router)
        dp.include_router(manage_users.router)

        # And the run events dispatching
        print("🤖 Bot is running...")
        await dp.start_polling(bot)

    except Exception as e:
        print(f"Error in starting the bot: {e}")
        raise e
