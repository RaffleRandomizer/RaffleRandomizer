
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot_data.models import Language
from bot.data import bot_data as td
from bot_data.services.text import get_text_by_language_and_key
from aiogram.types.web_app_info import WebAppInfo

__all__ = [
    'user_channels',
    "giv_user_channels",
    "giv_user_channels_post_now",
    "cancel",
    "channel_menu",
    "select_button_type",
    "no_sub_channels",
    "enough_channels",
    "giv_dt",
    "how_to_end_giv",
    "get_giv_kb",
    "save_giv",
    "yes",
    "pub_now_or_no",
    "lot_kb",
    "edit_lot_cond",
    "end_giv_now_or_not"
    ]

async def user_channels(user_channels_list: list, lang:Language):
    keyboard = InlineKeyboardBuilder()
    for channel in user_channels_list:
        keyboard.button(
            text=channel.title,
            callback_data=f'place_id:{channel.id}'
        )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_ADD_CHANNEL, lang=lang),
        callback_data=td.IK_ADD_CHANNEL,
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def giv_user_channels(user_channels_list: list):
    keyboard = InlineKeyboardBuilder()
    for channel in user_channels_list:
        keyboard.button(
            text=channel.title,
            callback_data=f'giv_channel_{channel.id}'
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


async def giv_user_channels_post_now(user_channels_list: list, giv_pk:str):
    keyboard = InlineKeyboardBuilder()
    for channel in user_channels_list:
        keyboard.button(
            text=channel.title,
            callback_data=f'giv_now_{channel.id}|{giv_pk}'
        )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def cancel(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_CANCEL, lang=lang),
        callback_data=td.IK_CANCEL,
    )
    return keyboard.as_markup()

async def cancel_action(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_CANCEL_ACTION, lang=lang),
        callback_data=td.IK_CANCEL_ACTION,
    )
    return keyboard.as_markup()

async def channel_menu(place_pk:str|int, lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_UPD_CH_NAME, lang=lang),
        callback_data=f"upd_{place_pk}",
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_DEL_CH_NAME, lang=lang),
        callback_data=f"del_{place_pk}",
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def select_button_type(lang:Language):
    keyboard = InlineKeyboardBuilder()
    for key in td.SELECT_BUTTON_TYPE:
        keyboard.button(
            text=await get_text_by_language_and_key(key=key, lang=lang),
            callback_data=key,
        )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def no_sub_channels(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_NO_SUB_CHANNELS, lang=lang),
        callback_data=td.IK_NO_SUB_CHANNELS,
    )
    return keyboard.as_markup()

async def enough_channels(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_GIV_ENOUGH_CH, lang=lang),
        callback_data=td.IK_GIV_ENOUGH_CH,
    )
    return keyboard.as_markup()

async def giv_dt(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_NOW, lang=lang),
        callback_data=td.IK_NOW,
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_PLAN_GIV, lang=lang),
        callback_data=td.IK_PLAN_GIV,
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def how_to_end_giv(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_END_BY_DT, lang=lang),
        callback_data=td.IK_END_BY_DT,
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_END_BY_COUNT, lang=lang),
        callback_data=td.IK_END_BY_COUNT,
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def get_giv_kb(kb_text:str, giv_uuid:str = None):
    keyboard = InlineKeyboardBuilder()
    if giv_uuid is not None:
        keyboard.button(
            text=kb_text,
            callback_data=f"z_{giv_uuid}",
        )
    else:
        keyboard.button(
            text=kb_text,
            callback_data=f"qwe",
        )
    return keyboard.as_markup()

async def save_giv(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_SAVE_GIV, lang=lang),
        callback_data=td.IK_SAVE_GIV,
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_CANCEL_GIV, lang=lang),
        callback_data=td.IK_CANCEL_GIV,
    )
    keyboard.adjust(1)
    return keyboard.as_markup()



async def yes(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_YES, lang=lang),
        callback_data=td.IK_YES,
    )
    return keyboard.as_markup()

async def pub_now_or_no(channel_id, lang:Language, giv_pk:str):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_CANCEL_PUB_NOW, lang=lang),
        callback_data=f"{td.IK_CANCEL_PUB_NOW}",
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_PUB_NOW_TO, lang=lang),
        callback_data=f"{td.IK_PUB_NOW_TO}_{channel_id}|{giv_pk}",
    )
    keyboard.adjust(2)
    return keyboard.as_markup()


async def lot_kb(lang:Language, status: str, giv_pk:str):
    keyboard = InlineKeyboardBuilder()
    if status == "waiting":
        keyboard.button(
            text=await get_text_by_language_and_key(key=td.IK_CHANGE_COND, lang=lang),
            callback_data=f"{td.IK_CHANGE_COND}_{giv_pk}",
        )
    elif status == "public":
        keyboard.button(
            text=await get_text_by_language_and_key(key=td.IK_CHANGE_COND, lang=lang),
            callback_data=f"{td.IK_CHANGE_COND}_{giv_pk}",
        )
        keyboard.button(
            text=await get_text_by_language_and_key(key=td.IK_END_NOW, lang=lang),
            callback_data=f"{td.IK_END_NOW}_{giv_pk}",
        )
    elif status == "end":
        keyboard.button(
            text=await get_text_by_language_and_key(key=td.IK_GET_LINK, lang=lang),
            callback_data=f"{td.IK_GET_LINK}_{giv_pk}",
        )
        keyboard.button(
            text=await get_text_by_language_and_key(key=td.IK_GET_EXCEL, lang=lang),
            callback_data=f"{td.IK_GET_EXCEL}_{giv_pk}",
        )
        keyboard.button(
            text=await get_text_by_language_and_key(key=td.IK_ADD_WINNERS, lang=lang),
            callback_data=f"{td.IK_ADD_WINNERS}_{giv_pk}",
        )

    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_DEL_LOT, lang=lang),
        callback_data=f"{td.IK_DEL_LOT}_{giv_pk}",
    )
    keyboard.adjust(1)
    return keyboard.as_markup()

async def edit_lot_cond(lang:Language):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_EBT, lang=lang),
        callback_data=f"{td.IK_EBT}",
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_BCU, lang=lang),
        callback_data=f"{td.IK_BCU}",
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_CPN_2, lang=lang),
        callback_data=f"{td.IK_CPN_2}",
    )
    keyboard.adjust(1)
    return keyboard.as_markup()


async def end_giv_now_or_not(lang:Language, giv_pk: str|int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_END_GIV, lang=lang),
        callback_data=f"{td.IK_END_GIV}_{giv_pk}",
    )
    keyboard.button(
        text=await get_text_by_language_and_key(key=td.IK_END_GIV_CANCEL, lang=lang),
        callback_data=f"{td.IK_END_GIV_CANCEL}",
    )
    keyboard.adjust(2)
    return keyboard.as_markup()