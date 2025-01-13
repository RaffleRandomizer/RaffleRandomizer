from dataclasses import dataclass
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

@dataclass
class MessageData:
    telegram_id: int|str
    text: str
    state: FSMContext|None = None
    keyboard: types.InlineKeyboardMarkup | types.ReplyKeyboardMarkup | None = None
    this_message_id: str|int = None
    main_message: bool = True
    file: types.InputFile = None
    file_id: str = None
    delete_income_message: bool = False
    delete_previous_main_mesage:bool = False
    add_to_delete_list: bool = False
    clear_delete_list: bool = False
    markdown:bool =False
    delete_on_edit:bool = True
    parse_mode: ParseMode = ParseMode.HTML
    reply_to_message_id: str|int = None