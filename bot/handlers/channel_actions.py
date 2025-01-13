from aiogram import types, Router, filters, F
from aiogram.fsm.context import FSMContext
from telegram.services import telegram_user as tus
from bot.data import bot_data as td
from bot.data.dataclasses import MessageData
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.utils import message_worker as mw
from bot_data.services import text as ts
from bot.config.loader import bot
from telegram.models import TelegramUser
from pprint import pprint
from aiogram.enums import ChatMemberStatus
from randomizer.services import chat as cs
from bot.states.DefaultState import DefaultState

from aiogram.enums import ParseMode


ch_actions = Router()

@ch_actions.callback_query(F.data.startswith('upd_'))
async def update_chanel_name(call:types.CallbackQuery, state:FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    place_pk = call.data.split('_')[1]
    place_obj = await cs.get_place_by_pk(place_pk=place_pk)
    place = await bot.get_chat(chat_id=place_obj.place_id)
    is_user_admin = await bot.get_chat_member(chat_id=place.id, user_id=user.telegram_id)
    text = await ts.get_text_by_language_and_key(key=td.NOT_ADMIN, lang=user.selected_language)
    if is_user_admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        current_data = {"title":place.title, "type": place.type, "username": place.username}
        old_data = {"title":place_obj.title, "type": place_obj.place_type, "username":place_obj.channel_username}
        need_update = False
        for key, value in current_data.items():
            if value != old_data[key]:
                need_update = True
                break
        if need_update:
            await cs.update_place_type_and_title(
                place_id=place_obj.place_id, 
                title=current_data.get('title'),
                place_type=current_data.get('type'),
                username=current_data.get('username'),)
            text = await ts.get_text_by_language_and_key(key=td.HAVE_CHANGES, lang=user.selected_language)
        else:
            text = await ts.get_text_by_language_and_key(key=td.NO_CHANGES, lang=user.selected_language)
    await call.answer(text=text)



@ch_actions.callback_query(F.data.startswith('del_'))
async def delete_chanel(call:types.CallbackQuery, state:FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    place_pk = call.data.split('_')[1]
    place_obj = await cs.get_place_by_pk(place_pk=place_pk)
    is_user_admin = await bot.get_chat_member(chat_id=place_obj.place_id, user_id=user.telegram_id)
    text = await ts.get_text_by_language_and_key(key=td.NOT_ADMIN, lang=user.selected_language)
    if is_user_admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
        text = await ts.get_text_by_language_and_key(key=td.DELETE_CHANNEL, lang=user.selected_language)
        command = f"`/delete_channel {place_obj.place_id}`"
        text = text.format(command=command)
        md = MessageData(
            telegram_id=telegram_id,
            text=text,
            state=state,
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await mw.try_send_message(md=md)
        text = None
    await call.answer(text=text)


@ch_actions.callback_query(F.data == td.IK_ADD_CHANNEL)
async def add_channel(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    await state.set_state(DefaultState.GET_CHANNEL_DATA)
    print(await state.get_state())
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.ADD_CHANNEL, lang=user.selected_language)
    keyboard = await ik.cancel(lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
        keyboard=keyboard
    )
    await mw.try_send_message(md=md)
    await call.answer()


@ch_actions.message(filters.StateFilter(DefaultState.GET_CHANNEL_DATA))
async def add_channel_by_username(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    if message.forward_from_chat:
        try:
            chat = await bot.get_chat(chat_id=message.forward_from_chat.id)
        except Exception as e:
            text = await ts.get_text_by_language_and_key(key=td.NO_CHANNEL, lang=user.selected_language)
            await mw.try_send_message(md=MessageData(text=text, telegram_id=telegram_id, state=state))
            return
    elif "@" in message.text:
        channel_username = message.text
        try:
            chat = await bot.get_chat(chat_id=channel_username)
        except Exception as e:
            text = await ts.get_text_by_language_and_key(key=td.NO_CHANNEL, lang=user.selected_language)
            await mw.try_send_message(md=MessageData(text=text, telegram_id=telegram_id, state=state))
            return
    elif "/" in message.text:
        channel_id = message.text.split("/")[-2]
        channel_id = f"-100{channel_id}"
        chat = await bot.get_chat(chat_id=channel_id)
    else:
        text = await ts.get_text_by_language_and_key(key=td.WRONG_FORMAT, lang=user.selected_language)
        await mw.try_send_message(md=MessageData(text=text, telegram_id=telegram_id, state=state))
        return

    
    await check_channel_and_send_message(channel=chat, state=state, user=user, telegram_id=telegram_id)


async def check_channel_and_send_message(channel, state: FSMContext, user: TelegramUser, telegram_id:str):
    pprint(channel.model_dump())
    me = await bot.get_me()
    try:
        is_bot_admin = await bot.get_chat_member(chat_id=channel.id, user_id=me.id)
        if is_bot_admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            is_bot_admin = True
    except Exception as e:
        is_bot_admin = False
    keyboard = None
    if is_bot_admin:
        is_user_admin = False
        user_status = await bot.get_chat_member(chat_id=channel.id, user_id=telegram_id)
        if user_status.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            is_user_admin = True
        if is_user_admin:
            channel_obj = await cs.get_place(place_id=channel.id)
            if not channel_obj:
                title = channel.title
                place_type = channel.type
                place_id = channel.id
                username = channel.username
                channel_obj = await cs.create_place(
                    title=title, 
                    place_id=place_id, 
                    place_type=place_type, 
                    username=username,
                    admin_rights=True) # создать канал
            result = await cs.update_place_admins(place_id=channel_obj.place_id, admins_list=[user])
            if not result:
                text = await ts.get_text_by_language_and_key(key=td.ALREADY_ADDED_CHANNEL, lang=user.selected_language)
                keyboard = await ik.cancel(lang=user.selected_language)
            else:
                text = await ts.get_text_by_language_and_key(key=td.CHANNEL_ADDED, lang=user.selected_language)
                text = text.format(name=channel.title)   
                await state.set_state(DefaultState.DEFAULT_STATE)
        else:
            text = await ts.get_text_by_language_and_key(key=td.ERROR_NOT_ADMIN, lang=user.selected_language)
    else:
        text = await ts.get_text_by_language_and_key(key=td.BOT_NOT_ADMIN, lang=user.selected_language)
        
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
        keyboard=keyboard,
    )
    await mw.try_send_message(md=md)

@ch_actions.callback_query(F.data == td.IK_CANCEL and (filters.StateFilter(DefaultState.GET_CHANNEL_DATA, DefaultState.GET_GIV_TEXT_AND_FILES)))
async def cancel(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.CANCEL, lang=user.selected_language)
    keyboard = await rk.main_menu(lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
        keyboard=keyboard,
    )
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
    await mw.try_send_message(md=md)
    await state.set_state(DefaultState.DEFAULT_STATE)
    await call.answer()


