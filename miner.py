import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand

from bot import bot, dp
from environs import Env

from data_bases import models
from handlers import started_handler, deposit_handler

env = Env()
env.read_env()

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def set_default_commands():
    await bot.set_my_commands(
        [
            BotCommand(command='/start', description='Перезапустить бота'),
        ]
    )


async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start', description='Перезапустить бота')]

    await bot.set_my_commands(main_menu_commands)

async def main():

    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    '''Подключаем базу данных'''
    await models.db_connect()

    # Регистриуем роутеры в диспетчере
    dp.include_router(deposit_handler.router)
    dp.include_router(started_handler.router)
    
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

