from bot.config.loader import bot
import logging
from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode



async def send_notification(telegram_ids:list, text):
    TOKEN = getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.info(f"Sending notification to {telegram_ids}")
    for telegram_id in telegram_ids:
        try:
            logging.info(f"Sending notification to {telegram_id}")
            await bot.send_message(
                chat_id=telegram_id,
                text=text
            )
        except Exception as e:
            logging.error(f"Error while sending notification to {telegram_id}: {e}")