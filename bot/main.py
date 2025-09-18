import asyncio
import logging
from sys import stdout

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers import other, user
from db import init_db

def init_logger(config: Config):
    formatter = logging.Formatter(
        fmt=config.log.format,
        style=config.log.style  # type: ignore #??
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(config.log.level)

    logging.basicConfig(
        level=logging.DEBUG,
        format=config.log.format,
        stream=stdout
    )


async def main() -> None:

    config: Config = load_config()
    init_logger(config=config)

    await init_db()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),

    )

    dp = Dispatcher()

    dp.include_router(user.router)
    dp.include_router(other.router)

    await dp.start_polling(bot)

    logging.info("Handling command...")


if __name__ == "__main__":
    asyncio.run(main())
