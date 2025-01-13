from aiogram import types, Router, filters, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from telegram.services import telegram_user as tus
from bot.data import bot_data as td
from bot.data.dataclasses import MessageData
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.utils import message_worker as mw
from bot_data.services import text as ts
from bot.states.DefaultState import DefaultState
from randomizer.services import givs as gs
from datetime import datetime
from bot.config.loader import moscow_tz
from typing import List
from randomizer.models import Giveaway
import logging


main_menu = Router()


async def check_cancel(state:FSMContext, telegram_id:str):
    current_state = await state.get_state()
    if current_state != DefaultState.DEFAULT_STATE and current_state is not None:
        await state.update_data({
            "giv_text": None,
            "video_id": None,
            "video_name": None,
            "photo": None,
            "button_type_text": None,
            "channels_list": [],
            "winners_count": None,
            "post_channel_id": None,
            "post_giv_now": None,
            "post_giv_dt": None,
            "giv_results_dt": None,
            "giv_results_count": None,
        })
        await send_cancel(state=state, telegram_id=telegram_id)

@main_menu.message(lambda message: ts.get_key_by_text_sync(message.text) in td.MAIN_MENU_BUTTONS)
async def main_menu_button_pressed(message: types.Message, state: FSMContext, telegram_id:str):
    key = await ts.get_key_by_text(message.text)
    if key in td.MAIN_MENU_BUTTONS:
        await check_cancel(state=state, telegram_id=telegram_id)
        await HANDLERS_BY_KEY[key](message=message, state=state, telegram_id=telegram_id)
        
        
async def my_channels(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    user_channels = await tus.get_user_places(telegram_id=telegram_id)
    text = await ts.get_text_by_language_and_key(key=td.MY_CHANNELS, lang=user.selected_language)
    keyboard = await ik.user_channels(user_channels_list=user_channels, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        keyboard=keyboard,
        state=state,
        text=text,
    )
    await mw.try_send_message(md=md)

@main_menu.callback_query(F.data.startswith("place_id:"))
async def channel_menu(call:types.CallbackQuery, state: FSMContext, telegram_id:str):
    channel_pk = call.data.split(":")[1]
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.CHANNEL_MENU, lang=user.selected_language)
    keyboard = await ik.channel_menu(place_pk=channel_pk, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        keyboard=keyboard,
        state=state,
        text=text,
    )
    await mw.try_send_message(md=md)
    await call.answer()

async def my_givs(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    user_givs: List[Giveaway] = await gs.get_user_givs(user=user)
    text = await ts.get_text_by_language_and_key(key=td.MY_GIVS, lang=user.selected_language)
    now = datetime.now().astimezone(moscow_tz)
    givs_data = ""
    for giv in user_givs:
        giv_emoji = ""
        if giv.post_giv_dt.astimezone(moscow_tz) > now:
            giv_emoji = "🆕"
        elif giv.ended:
            giv_emoji = "🔵"
        else:
            giv_emoji = "🟢"
        command = f"/mylot{giv.pk}"
        giv_text = (giv.giv_text[:20] + "...") if len(giv.giv_text) > 20 else giv.giv_text
        result = f"{giv_emoji} {command} {giv_text}"
        givs_data += result + "\n"
    text = text.format(givs_data=givs_data)
    text = text.replace("<", "").replace(">", "")
    md = MessageData(telegram_id=telegram_id, state=state, text=text)
    await mw.try_send_message(md=md)
    

async def change_language(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    await tus.update_user_language(user=user)
    text = await ts.get_text_by_language_and_key(key=td.HELLO_MESSAGE, lang=user.selected_language)
    keyboard = await rk.main_menu(lang=user.selected_language)
    md = MessageData(
        telegram_id=user.telegram_id,
        state=state,
        text=text,
        keyboard=keyboard,
    )
    await mw.try_send_message(
        md=md
    )


async def create_giv(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    user_places = await tus.get_user_places(telegram_id=telegram_id)
    keyboard = None
    if user_places:
        text = await ts.get_text_by_language_and_key(key=td.GIV_CREATION, lang=user.selected_language)
        keyboard = await ik.cancel(lang=user.selected_language)
        await state.set_state(DefaultState.GET_GIV_TEXT_AND_FILES)
    else:
        text = await ts.get_text_by_language_and_key(key=td.NO_CHANNELS_ADDED, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        state=state,
        keyboard=keyboard,
        text=text,
    )
    await mw.try_send_message(md=md)


    
async def help(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.HELP_TEXT, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
    )
    await mw.try_send_message(md=md)

    
async def donate(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.SUPPORT, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
    )
    await mw.try_send_message(md=md)
    
HANDLERS_BY_KEY = {
    td.RK_MY_CHANNELS: my_channels,
    td.RK_MY_GIVS: my_givs,
    td.RK_CREATE_GIV: create_giv,
    td.RK_HELP: help,
    td.RK_SUPPORT: donate,
    td.RK_SWITCH_LANGUAGE: change_language,
}




async def send_cancel(state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.AUTO_CANCEL, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
    )
    await mw.try_send_message(md=md)
    await state.set_state(DefaultState.DEFAULT_STATE)



