from bot.config.loader import bot
from aiogram import types
from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

async def check_operator_in_chat(operator_id:str|int, chat_id:str|int):
    status = await bot.get_chat_member(chat_id=chat_id, user_id=operator_id)
    if isinstance(status, types.ChatMemberBanned) or isinstance(status, types.ChatMemberLeft):
        return False
    return True

async def leave_chat(chat_id: str|int):
    TOKEN = getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.leave_chat(chat_id=chat_id)