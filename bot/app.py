import logging
from aiogram import Dispatcher

from .config.loader import dp, bot
from . import handlers
import os
import django
import asyncio
from bot.middleware.default_mw import DefaultMiddleware

def run_bot():
    """Запускает процессы бота"""
    _setup_django()
    print("Bot start")
    for router in handlers.routers:
        dp.include_router(router)
    dp.message.middleware(DefaultMiddleware())
    dp.callback_query.middleware(DefaultMiddleware())
    asyncio.run(
        dp.start_polling(
            bot, on_shutdown=_on_shutdown
    ))


async def _on_shutdown(dispatcher: Dispatcher):
    """Ожидает и закрывает хранилище dispatcher"""
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def _setup_django():
    """Установка окружения Django внутри бота"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()