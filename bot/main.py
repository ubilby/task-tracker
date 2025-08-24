import asyncio
import logging
from sys import stdout

from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import other, user


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    formatter = logging.Formatter(
        fmt=config.log.format,
        style=config.log.style  # Учитываем стиль из конфига #type: ignore
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(config.log.level)

    # Задаём базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.DEBUG,
        format=config.log.format,
        stream=stdout
    )

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.bot.token)
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user.router)
    dp.include_router(other.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    logging.info('Handling command...')


if __name__ == '__main__':
    asyncio.run(main())