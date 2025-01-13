from aiogram import types, Router, filters, F
from aiogram.fsm.context import FSMContext
from telegram.services import telegram_user as tus
from bot.data import bot_data as td
from bot.data.dataclasses import MessageData
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.utils import message_worker as mw
from bot_data.services import text as ts
from bot.config.loader import bot, moscow_tz
from telegram.models import TelegramUser
from pprint import pprint
from aiogram.enums import ChatMemberStatus
from randomizer.services import chat as cs
from bot.states.DefaultState import DefaultState
from bot.utils.date_worker import (
    get_dts, 
    is_valid_datetime,
    is_future_datetime,
    get_now_plus_one_minute,
    get_datiteme_object,
    is_post_before_results_datetime,
    get_datetime_str,
    )
from randomizer_bot.settings import TEMP_PATH
import os
from bot.handlers.commands import command_start
from aiogram.enums import ParseMode
from randomizer.services import givs as gs
from datetime import datetime
from bot.utils import giv as giv_s

giv_actions = Router()


@giv_actions.message(filters.StateFilter(DefaultState.GET_GIV_TEXT_AND_FILES), F.text)
async def giv_text(message: types.Message, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_text = message.html_text
    await state.update_data({
        'giv_text': giv_text,
    })
    text = await ts.get_text_by_language_and_key(key=td.GIV_TEXT_ADDED, lang=user.selected_language)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state
    )
    await mw.try_send_message(md=md)
    await select_button_type(message=message, state=state, user=user)

@giv_actions.message(filters.StateFilter(DefaultState.GET_GIV_TEXT_AND_FILES), F.video)
async def giv_text_and_video(message: types.Message, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_text = message.html_text
    video_id = message.video.file_id
    video_name = message.video.file_name
    await state.update_data({
        'giv_text': giv_text,
        "video_id": video_id,
        "video_name": video_name,
    })
    text_video = await ts.get_text_by_language_and_key(key=td.GIV_VIDEO_ADDED, lang=user.selected_language)
    md_video = MessageData(
        text=text_video,
        telegram_id=telegram_id,
        state=state
    )
    await mw.try_send_message(md=md_video)
    if giv_text:
        text = await ts.get_text_by_language_and_key(key=td.GIV_TEXT_ADDED, lang=user.selected_language)
        md = MessageData(
            text=text,
            telegram_id=telegram_id,
            state=state
        )
        await mw.try_send_message(md=md)
    print("giv_video_handled")
    await select_button_type(message=message, state=state, user=user)

@giv_actions.message(filters.StateFilter(DefaultState.GET_GIV_TEXT_AND_FILES), F.photo)
async def giv_text_and_photo(message: types.Message, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_text = message.html_text
    photo = message.photo[-1]
    await state.update_data({
        'giv_text': giv_text,
        "photo": photo,
    })
    print("giv_photo_handled")
    text_photo = await ts.get_text_by_language_and_key(key=td.GIV_PHOTO_ADDED, lang=user.selected_language)
    md_video = MessageData(
        text=text_photo,
        telegram_id=telegram_id,
        state=state
    )
    await mw.try_send_message(md=md_video)
    if giv_text:
        text = await ts.get_text_by_language_and_key(key=td.GIV_TEXT_ADDED, lang=user.selected_language)
        md = MessageData(
            text=text,
            telegram_id=telegram_id,
            state=state
        )
        await mw.try_send_message(md=md)
    await select_button_type(message=message, state=state, user=user)

async def select_button_type(message: types.Message, state:FSMContext, user: TelegramUser):
    text = await ts.get_text_by_language_and_key(key=td.GIV_GET_BUTTON_TYPE, lang=user.selected_language)
    keyboard = await ik.select_button_type(lang=user.selected_language)
    await state.set_state(DefaultState.GET_GIV_BUTTON_TYPE)
    md = MessageData(
        text=text,
        telegram_id=user.telegram_id,
        state=state,
        keyboard=keyboard
    )
    await mw.try_send_message(md=md)

@giv_actions.callback_query(lambda call: call.data in td.SELECT_BUTTON_TYPE, filters.StateFilter(DefaultState.GET_GIV_BUTTON_TYPE))
async def select_existed_type(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    button_type_text = await ts.get_text_by_language_and_key(key=call.data, lang=user.selected_language)
    print("Текст для кнопки", button_type_text)
    await state.update_data({
        'button_type_text': button_type_text,
    })
    text = await ts.get_text_by_language_and_key(key=td.BUTTON_TEXT_SAVE, lang=user.selected_language)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state,
    )
    await mw.try_send_message(md=md)
    await add_sub_channels(state=state, user=user)
    await call.answer()

@giv_actions.message(F.text or F.caption, filters.StateFilter(DefaultState.GET_GIV_BUTTON_TYPE))
async def enter_new_button_text(message: types.Message, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    button_type_text = message.text
    await state.update_data({
        'button_type_text': button_type_text,
    })
    print("Текст для кнопки", button_type_text)
    text = await ts.get_text_by_language_and_key(key=td.BUTTON_TEXT_SAVE, lang=user.selected_language)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state,
    )
    await mw.try_send_message(md=md)
    await add_sub_channels(state=state, user=user)
    


async def add_sub_channels(state:FSMContext, user: TelegramUser):
    text = await ts.get_text_by_language_and_key(key=td.GIV_ADD_CHANELS_TO_SUB, lang=user.selected_language)
    keyboard = await ik.no_sub_channels(lang=user.selected_language)
    await state.set_state(DefaultState.GET_GIV_CHANNELS_SUB)
    md = MessageData(
        text=text,
        telegram_id=user.telegram_id,
        state=state,
        keyboard=keyboard
    )
    await mw.try_send_message(md=md)

@giv_actions.message(filters.StateFilter(DefaultState.GET_GIV_CHANNELS_SUB))
async def add_channel_by_username(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    print(234234)
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
    await check_channel_and_send_message(channel=chat, state=state, user=user, telegram_id=telegram_id)




async def check_channel_and_send_message(channel, state: FSMContext, user: TelegramUser, telegram_id:str):
    me = await bot.get_me()
    try:
        is_bot_admin = await bot.get_chat_member(chat_id=channel.id, user_id=me.id)
        if is_bot_admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            is_bot_admin = True
    except Exception as e:
        is_bot_admin = False
    data = await state.get_data()
    channels_list = data.get("channels_list", [])
    keyboard = None
    if is_bot_admin:
        channel_obj = await cs.get_place(place_id=channel.id)
        print(channel_obj)
        if channel_obj is not None:
            print(channels_list, channel_obj.pk)
            if channel_obj.pk in channels_list:
                text = await ts.get_text_by_language_and_key(key=td.ALREADY_ADDED_CHANNEL, lang=user.selected_language)
            else:
                channels_list.append(channel_obj.pk)
                text = await ts.get_text_by_language_and_key(key=td.GIV_CHANNEL_ADDED, lang=user.selected_language)
            print("Добавляем канал существующий в админке")
        else:
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
            if channel_obj.pk in channels_list:
                text = await ts.get_text_by_language_and_key(key=td.ALREADY_ADDED_CHANNEL, lang=user.selected_language)
            else:
                channels_list.append(channel_obj.pk)
                text = await ts.get_text_by_language_and_key(key=td.GIV_CHANNEL_ADDED, lang=user.selected_language)
            print("Создаем новый канал")
        
        keyboard = await ik.enough_channels(lang=user.selected_language)
    else:
        text = await ts.get_text_by_language_and_key(key=td.BOT_NOT_ADMIN, lang=user.selected_language)
    
    await state.update_data({
        "channels_list": channels_list,
    })
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
        keyboard=keyboard,
    )
    await mw.try_send_message(md=md)


@giv_actions.callback_query(lambda call: call.data in [td.IK_NO_SUB_CHANNELS, td.IK_GIV_ENOUGH_CH], filters.StateFilter(DefaultState.GET_GIV_CHANNELS_SUB))
async def sub_channels_saved_zero_or_more(call:types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.CHANNELS_SAVED, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    await call.answer()
    text_winners_count = await ts.get_text_by_language_and_key(key=td.WINNERS_COUNT, lang=user.selected_language)
    await state.set_state(DefaultState.GET_WINNERS_COUNT)
    md_winners_count = MessageData(text=text_winners_count, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md_winners_count)


@giv_actions.message(F.text, filters.StateFilter(DefaultState.GET_WINNERS_COUNT))
async def get_winners_count(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    try:
        winners_count = int(message.text)
        if winners_count < 0:
            winners_count *= -1    
        if winners_count > 1000:
            text = await ts.get_text_by_language_and_key(key=td.GIV_TOO_MUCH_WINNERS, lang=user.selected_language)
            md = MessageData(text=text, telegram_id=telegram_id, state=state)
            await mw.try_send_message(md=md)
            return
        
        await state.update_data({
                "winners_count": winners_count,
            })
        text = await ts.get_text_by_language_and_key(key=td.WINNERS_COUNT_SAVED, lang=user.selected_language)
        text = text.format(count=winners_count)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md=md)
    except Exception as e:
        print(e)
        text = await ts.get_text_by_language_and_key(key=td.NEED_NUMBER, lang=user.selected_language)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md=md)
        return
    text = await ts.get_text_by_language_and_key(key=td.GIV_SELECT_CHANNEL, lang=user.selected_language)
    user_channels = await tus.get_user_places(telegram_id=telegram_id)
    keyboard = await ik.giv_user_channels(user_channels_list=user_channels)
    md = MessageData(text=text, telegram_id=telegram_id, state=state, keyboard=keyboard)
    await mw.try_send_message(md=md)
    await state.set_state(DefaultState.SELECT_GIV_CHANNEL)


@giv_actions.callback_query(F.data.startswith("giv_channel_"), filters.StateFilter(DefaultState.SELECT_GIV_CHANNEL))
async def select_giv_channel(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    channel_id = call.data.split("_")[-1]
    channel = await cs.get_place_by_pk(place_pk=channel_id)
    me = await bot.get_me()
    try:
        is_bot_admin = await bot.get_chat_member(chat_id=channel.place_id, user_id=me.id)
        if is_bot_admin.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]:
            is_bot_admin = True
    except Exception as e:
        is_bot_admin = False
    keyboard = None
    if is_bot_admin:
        print("Выбран канал", channel_id)
        await state.update_data({
            "post_channel_id": channel_id,
        })
        text = await ts.get_text_by_language_and_key(key=td.GIV_CHANNEL_SELECTED, lang=user.selected_language)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await call.answer()
        await state.set_state(DefaultState.GET_TYPE_OF_DT_GIV)
    else:
        text = await ts.get_text_by_language_and_key(key=td.BOT_NOT_ADMIN, lang=user.selected_language)

    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
        keyboard=keyboard,
    )
    await mw.try_send_message(md=md)
    if is_bot_admin:
        text = await ts.get_text_by_language_and_key(key=td.GIV_SELECT_DT, lang=user.selected_language)
        keyboard = await ik.giv_dt(lang=user.selected_language)
        md = MessageData(
            telegram_id=telegram_id,
            text=text,
            state=state,
            keyboard=keyboard,
        )
        await mw.try_send_message(md=md)
   
@giv_actions.callback_query(F.data == td.IK_PLAN_GIV, filters.StateFilter(DefaultState.GET_TYPE_OF_DT_GIV))
async def pub_giv_plan(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.GIV_WHEN_PLAN_DT, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    await call.answer()
    text_examples = await ts.get_text_by_language_and_key(key=td.GIV_TD_EXAMPLES, lang=user.selected_language)
    dates = await get_dts()
    text_examples = text_examples.format(**dates)
    md_examples = MessageData(text=text_examples, state=state, telegram_id=telegram_id, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(DefaultState.GIV_WAITING_END_DT)
    await mw.try_send_message(md=md_examples)   


@giv_actions.callback_query(F.data == td.IK_NOW, filters.StateFilter(DefaultState.GET_TYPE_OF_DT_GIV))
async def pub_giv_now(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.GIV_DT_SELECTED, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await state.update_data({
            "post_giv_now": True, # сохранится текст bool не будет работать
        })
    await mw.try_send_message(md=md)
    await call.answer()
    text_end_giv_type = await ts.get_text_by_language_and_key(key=td.GIV_HOW_TO_END, lang=user.selected_language)
    keyboard = await ik.how_to_end_giv(lang=user.selected_language)
    md_end = MessageData(text=text_end_giv_type, keyboard=keyboard, state=state, telegram_id=telegram_id)
    await state.set_state(DefaultState.GET_TYPE_OF_END_GIV)
    await mw.try_send_message(md=md_end)


@giv_actions.message(F.text, filters.StateFilter(DefaultState.GIV_WAITING_END_DT))
async def check_is_date_correct(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True) 
    dt = message.text
    is_valid = is_valid_datetime(date_time_str=dt)
    if is_valid:
        if is_future_datetime(date_time_str=dt):
            key=td.GIV_DT_SELECTED
            await state.update_data({
                "post_giv_dt": dt,
            })
        else:
            is_valid = False
            key = td.GIV_DT_NOT_FUTURE
    else:
        key=td.GIV_WRONG_DT_FORMAT
    
    text = await ts.get_text_by_language_and_key(key=key, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    if is_valid:
        text_end_giv_type = await ts.get_text_by_language_and_key(key=td.GIV_HOW_TO_END, lang=user.selected_language)
        keyboard = await ik.how_to_end_giv(lang=user.selected_language)
        md_end = MessageData(text=text_end_giv_type, keyboard=keyboard, state=state, telegram_id=telegram_id)
        await state.set_state(DefaultState.GET_TYPE_OF_END_GIV)
        await mw.try_send_message(md=md_end)

@giv_actions.callback_query(F.data == td.IK_END_BY_DT, filters.StateFilter(DefaultState.GET_TYPE_OF_END_GIV))
async def end_giv_by_dt(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.GIV_WHEN_SELECT_WINER, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    await call.answer()
    text_examples = await ts.get_text_by_language_and_key(key=td.GIV_TD_EXAMPLES, lang=user.selected_language)
    dates = await get_dts()
    text_examples = text_examples.format(**dates)
    md_examples = MessageData(text=text_examples, state=state, telegram_id=telegram_id, parse_mode=ParseMode.MARKDOWN_V2)
    await state.set_state(DefaultState.GIV_WAITING_SELECT_DT)
    await mw.try_send_message(md=md_examples)  


@giv_actions.message(F.text, filters.StateFilter(DefaultState.GIV_WAITING_SELECT_DT))
async def check_is_date_correct(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True) 
    dt = message.text
    is_valid = is_valid_datetime(date_time_str=dt)
    if is_valid:
        if is_future_datetime(date_time_str=dt):
            data = await state.get_data()
            post_dt_str = data.get("post_giv_dt")
            post_now = data.get("post_giv_now")
            if post_now:
                post_dt_obj = await get_now_plus_one_minute()
                post_dt_str = await get_datetime_str(date=post_dt_obj)
            result_dt = get_datiteme_object(date=dt)
            post_dt = get_datiteme_object(date=post_dt_str)
            if is_post_before_results_datetime(results_dt=result_dt, post_dt=post_dt):
                key=td.GIV_DT_SELECT_WINNER
                await state.update_data({
                    "giv_results_dt": dt,
                })
            else:
                is_valid = False
                key = td.GIV_POST_BEFORE_RESULTS
        else:
            is_valid = False
            key = td.GIV_DT_NOT_FUTURE
    else:
        key=td.GIV_WRONG_DT_FORMAT
    
    text = await ts.get_text_by_language_and_key(key=key, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    if is_valid:
        await send_example_and_save_or_not(message=message, state=state, user=user)

@giv_actions.callback_query(F.data == td.IK_END_BY_COUNT, filters.StateFilter(DefaultState.GET_TYPE_OF_END_GIV))
async def end_giv_by_count(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.GIV_END_BY_COUNT, lang=user.selected_language)
    await call.answer()
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    await state.set_state(DefaultState.GIV_WAITING_COUNT_USERS)

@giv_actions.message(F.text, filters.StateFilter(DefaultState.GIV_WAITING_COUNT_USERS))
async def giv_waiting_count_users(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    try:
        users_count = int(message.text)
        data = await state.get_data()
        if users_count < 0:
            users_count *= -1
        if winners_count:=data.get("winners_count", None): 
            if users_count < int(winners_count):
                text = await ts.get_text_by_language_and_key(key=td.GIV_PARTS_LESS_THAN_WINNERS, lang=user.selected_language)
                md = MessageData(text=text, telegram_id=telegram_id, state=state)
                await mw.try_send_message(md=md)
                return
        await state.update_data({
            "giv_results_count": users_count,
        })
        text = await ts.get_text_by_language_and_key(key=td.GIV_END_USERS_COUNT, lang=user.selected_language)
        text = text.format(count=users_count)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md=md)
        await send_example_and_save_or_not(message=message, state=state, user=user)
    except Exception as e:
        print(e)
        text = await ts.get_text_by_language_and_key(key=td.NEED_NUMBER, lang=user.selected_language)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md=md)
        return

async def send_example_and_save_or_not(message: types.Message, state: FSMContext, user:TelegramUser):
    data = await state.get_data()
    giv_text = data.get("giv_text", "")
    video_id = data.get("video_id", False)
    photo = data.get("photo", False)
    button_type_text = data.get("button_type_text", False)
    winners_count = data.get("winners_count", 1)
    giv_results_dt = data.get("giv_results_dt", False)
    giv_results_count = data.get("giv_results_count", False)
    keyboard = await ik.get_giv_kb(kb_text=button_type_text)
    if photo:
        md = MessageData(
            text=giv_text,
            telegram_id=user.telegram_id,
            state=state,
            keyboard=keyboard,
            file_id=photo.file_id,
        )
        await mw.try_send_photo(md=md)
    elif video_id:
        md = MessageData(
            text=giv_text,
            telegram_id=user.telegram_id,
            state=state,
            keyboard=keyboard,
            file_id=video_id,
        )
        await mw.try_send_video(md=md)
    else:
        md = MessageData(
            text=giv_text,
            telegram_id=user.telegram_id,
            state=state,
            keyboard=keyboard,
        )
        await mw.try_send_message(md=md)

    if giv_results_count:
        key = td.CHECK_GIV_BEFORE_POST_COUNT
    else:
        key = td.CHECK_GIV_BEFORE_POST

    text = await ts.get_text_by_language_and_key(key=key, lang=user.selected_language)
    text = text.format(dt_or_count=giv_results_dt if giv_results_dt else giv_results_count, count=winners_count)
    keyboard = await ik.save_giv(lang=user.selected_language)
    await state.set_state(DefaultState.GIV_SAVE_OR_DELETE)
    md = MessageData(
        text=text,
        telegram_id=user.telegram_id,
        state=state,
        keyboard=keyboard,
    )
    await mw.try_send_message(md=md)




@giv_actions.callback_query(F.data == td.IK_SAVE_GIV, filters.StateFilter(DefaultState.GIV_SAVE_OR_DELETE))
async def save_giv(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.GIV_CREATED, lang=user.selected_language)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state,
    )
    data = await state.get_data()
    post_giv_now = data.get("post_giv_now", False)
    if post_giv_now:
        post_giv_dt = await get_now_plus_one_minute()
    else:
        post_giv_dt = get_datiteme_object(post_giv_dt)
    giv_results_dt = data.get("giv_results_dt", None)
    if giv_results_dt:
        giv_rerulst_dt_obj = get_datiteme_object(date=giv_results_dt)
        if giv_rerulst_dt_obj < post_giv_dt:
            await call.answer()
            text = await ts.get_text_by_language_and_key(key=td.RECREATE_GIV, lang=user.selected_language)
            await mw.try_send_message(md=MessageData(text=text, state=state, telegram_id=telegram_id))
            await command_start(message=call.message, state=state, telegram_id=telegram_id)
            return
    giv_uuid = await create_giveaway_logic(data=data, user=user)
    await mw.try_send_message(md=md)
    repost_text = await ts.get_text_by_language_and_key(key=td.GIV_REPOST_COMMAND, lang=user.selected_language)
    repost_text = repost_text.format(giv_uuid=giv_uuid.unique_id)
    md = MessageData(
        text=repost_text,
        telegram_id=telegram_id,
        state=state,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    await mw.try_send_message(md=md)
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
    await call.answer()
    await state.set_state(DefaultState.DEFAULT_STATE)

async def create_giveaway_logic(data, user: TelegramUser = None):
    giv_text = data.get("giv_text", "")
    video_id = data.get("video_id", False)
    video_name = data.get("video_name", False)
    photo = data.get("photo", False)
    button_type_text = data.get("button_type_text", "Участвовать")
    channels_list = data.get("channels_list", [])
    winners_count = data.get("winners_count", 1)
    post_channel_id = data.get("post_channel_id", False)
    post_giv_now = data.get("post_giv_now", False)
    post_giv_dt = data.get("post_giv_dt", False)
    giv_results_dt = data.get("giv_results_dt", None)
    giv_results_count = data.get("giv_results_count", None)
    downloaded_file_path = None
    file_name = None
    if photo:
        file = await bot.get_file(photo.file_id)
        file_name = f"{photo.file_id}.jpg"
        downloaded_file_path = os.path.join(TEMP_PATH, file_name)
    elif video_id:
        file = await bot.get_file(video_id)
        file_name = video_name
        downloaded_file_path = os.path.join(TEMP_PATH, video_name)
    if post_giv_now:
        post_giv_dt = await get_now_plus_one_minute()
    else:
        post_giv_dt = get_datiteme_object(post_giv_dt)
    giv_data = gs.GiveawayData(
        button_type_text=button_type_text,
        winners_count=winners_count,
        post_giv_dt=post_giv_dt,
        post_channel_id=post_channel_id,
        giv_text=giv_text,
        check_sub_channels=channels_list,
        giv_results_dt=giv_results_dt,
        giv_results_count=giv_results_count
    )
    if file_name:
        await bot.download_file(file.file_path, downloaded_file_path)
    return await gs.create_giveaway(file_path=downloaded_file_path, file_name=file_name, giv_data=giv_data, user=user)
    
@giv_actions.callback_query(F.data == td.IK_CANCEL_GIV, filters.StateFilter(DefaultState.GIV_SAVE_OR_DELETE))
async def cancel_giv(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.SURE_CANCEL, lang=user.selected_language)
    keyboard = await ik.yes(lang=user.selected_language)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state,
        keyboard=keyboard,
    )
    await mw.try_send_message(md=md)
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
    await call.answer()

@giv_actions.callback_query(F.data == td.IK_YES, filters.StateFilter(DefaultState.GIV_SAVE_OR_DELETE))
async def cancel_giv_aplied(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.GIV_CREATION_CANCELED, lang=user.selected_language)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state,
    )
    await mw.try_send_message(md=md)
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
    await call.answer()
    await state.set_state(DefaultState.DEFAULT_STATE)


@giv_actions.callback_query(F.data.startswith("giv_now_"))
async def post_giv_now_to(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    channel_id, giv_pk = call.data.split("_")[-1].split("|")
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.WILL_WE_PUB_GIV_TO, lang=user.selected_language)
    place = await cs.get_place_by_pk(place_pk=channel_id)
    text = text.format(place_name=place.title)
    keyboard = await ik.pub_now_or_no(channel_id=channel_id, lang=user.selected_language, giv_pk=giv_pk)
    md = MessageData(
        text=text,
        telegram_id=telegram_id,
        state=state,
        keyboard=keyboard,
    )
    await mw.try_send_message(md=md)
    await call.answer()

@giv_actions.callback_query(F.data.startswith(td.IK_PUB_NOW_TO))
async def post_giv_now_to(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    channel_id, giv_pk = call.data.split("_")[-1].split("|")
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    place = await cs.get_place_by_pk(place_pk=channel_id)
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    print("pub_now_to", place.title, giv)
    now = datetime.now().astimezone(moscow_tz)
    if giv.post_giv_dt.astimezone(moscow_tz) > now or giv.ended:
        text = await ts.get_text_by_language_and_key(key=td.GIV_ENDED_OR_NOT_POSTED_POSTLOT, lang=user.selected_language)
        await call.answer(text=text)
    else:
        await giv_s.send_giv_post_to_place_id(giv_obj=giv, place_id=place.place_id)
        await call.message.delete()

@giv_actions.callback_query(F.data.startswith("z_"))
async def get_in_pressed(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    giv_uuid = call.data.replace("z_", "")
    giv = await gs.get_giveaway_by_uuid(giv_uuid=giv_uuid)
    if giv:
        giv_channels = await gs.get_giv_check_channels(giv=giv)
        is_full_subbed = await check_sub(telegram_id=call.from_user.id, channel_ids=giv_channels)
        user = await gs.get_giveaway_part(telegram_id=call.from_user.id) or await gs.create_giveaway_part(
            telegram_id=call.from_user.id,
            name=call.from_user.full_name,
            username=call.from_user.username,
            bot_blocked=False,
        )
        givs_list = await gs.get_giv_participant_givs(telegram_id=call.from_user.id)
        if giv.ended:
            text = await ts.get_text_by_language_and_key(key=td.GIV_ALREADY_ENDED, lang=giv.creator.selected_language)
        elif giv in givs_list:
            text = await ts.get_text_by_language_and_key(key=td.ALREADY_IN, lang=giv.creator.selected_language)
        elif is_full_subbed:
            text = await ts.get_text_by_language_and_key(key=td.NOW_IN, lang=giv.creator.selected_language)
            await gs.add_new_giv_to_part(giv_part=user, giv_obj=giv)
            channel = giv.post_channels
            post_message = await gs.get_giv_post_by_place_and_giveaway(place=channel, giveaway=giv)
            giv_parts_count = await gs.get_parts_count(giv_obj=giv)
            kb_text = f"{giv.button_type_text} ({giv_parts_count})"
            keyboard = await ik.get_giv_kb(kb_text=kb_text, giv_uuid=giv.unique_id)
            try:
                await bot.edit_message_reply_markup(chat_id=channel.place_id, message_id=post_message.message_id, reply_markup=keyboard)
            except Exception as e:
                print(e)
            if giv_parts_count == giv.giv_results_count:
                await gs.update_giv_ended(giv_obj=giv)
        else:
            text = await ts.get_text_by_language_and_key(key=td.NOT_SUBBED, lang=giv.creator.selected_language)
        await call.answer(text=text, show_alert=True)

async def check_sub(telegram_id:str|int, channel_ids:list)-> bool | tuple:
    for chanel_id in channel_ids:
        try:
            status = await bot.get_chat_member(chat_id=chanel_id, user_id=telegram_id)
            if isinstance(status, types.ChatMemberBanned) or isinstance(status, types.ChatMemberLeft):
                return False
        except:
            return False
    return True

@giv_actions.callback_query(F.data.startswith(td.IK_CANCEL_PUB_NOW))
async def post_giv_now_to(call: types.CallbackQuery, state: FSMContext, telegram_id:str):
    await call.message.delete()