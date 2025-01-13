
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot.data import bot_data as td
from bot_data.services.text import get_text_by_language_and_key
from bot_data.models import Language

__all__ = [
    "main_menu"
]

async def main_menu(lang: Language = None):
    kb_list = [
        [KeyboardButton(text=await get_text_by_language_and_key(lang=lang, key=td.RK_CREATE_GIV)),
         KeyboardButton(text=await get_text_by_language_and_key(lang=lang, key=td.RK_MY_GIVS))],
        [KeyboardButton(text=await get_text_by_language_and_key(lang=lang, key=td.RK_MY_CHANNELS)),
         KeyboardButton(text=await get_text_by_language_and_key(lang=lang, key=td.RK_HELP))],
        [KeyboardButton(text=await get_text_by_language_and_key(lang=lang, key=td.RK_SWITCH_LANGUAGE))],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
    )

    return keyboard
