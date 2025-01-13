from randomizer.models import Giveaway, BotAddedToPlace
from bot.utils import message_worker as mw
from randomizer.services import givs as gs
from bot.data.dataclasses import MessageData
from bot.keyboards import inline as ik
from aiogram import types
from pprint import pprint
from bot_data.services import text as ts
from bot.data import bot_data as td
from aiogram.utils.deep_linking import create_start_link
import random
from bot.config.loader import bot
from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging




async def send_giv_post_to_place_id(giv_obj:Giveaway, place_id):
    giv_text = giv_obj.giv_text
    giv_photo = giv_obj.photo
    giv_video = giv_obj.video
    giv_uuid = giv_obj.unique_id
    parts = await gs.get_parts_count(giv_obj=giv_obj)
    btn_text = f"{giv_obj.button_type_text} ({parts})"
    keyboard = await ik.get_giv_kb(kb_text=btn_text, giv_uuid=giv_uuid)
    if giv_photo:
        photo = types.FSInputFile(path=giv_photo.path)
        if giv_obj.photo_id:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file_id=giv_obj.photo_id, file=photo)
            new_id, mes = await mw.try_send_photo(md=md)
            if new_id:
                await gs.update_giv_photo_id(giv_obj=giv_obj, photo_id=new_id)
        else:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file=photo)
            new_id, mes = await mw.try_send_photo(md=md)
            await gs.update_giv_photo_id(giv_obj=giv_obj, photo_id=new_id)
    elif giv_video:
        video = types.FSInputFile(path=giv_video.path)
        if giv_obj.video_id:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file_id=giv_obj.video_id, file=video)
            new_id, mes = await mw.try_send_video(md=md)
            if new_id:
                await gs.update_giv_video_id(giv_obj=giv_obj, video_id=new_id)
        else:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file=video)
            new_id, mes = await mw.try_send_video(md=md)
            await gs.update_giv_video_id(giv_obj=giv_obj, video_id=new_id)    
    else:
        md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard)
        mes = await mw.try_send_message(md=md)
    mes_id = mes.message_id
    chat_id = str(mes.chat.id).replace("-100", "")
    link = f"https://t.me/c/{chat_id}/{mes_id}"
    await gs.create_giv_post(place_id=place_id, giv_obj=giv_obj, mes_id=mes_id, mes_link=link)



async def send_giv_post_to_place_id_by_giv_pk(giv_pk:str, place_id:str ):
    giv_obj = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    giv_text = giv_obj.giv_text
    giv_photo = giv_obj.photo
    giv_video = giv_obj.video
    giv_uuid = giv_obj.unique_id
    parts = await gs.get_parts_count(giv_obj=giv_obj)
    btn_text = f"{giv_obj.button_type_text} ({parts})"
    keyboard = await ik.get_giv_kb(kb_text=btn_text, giv_uuid=giv_uuid)
    
    if giv_photo:
        photo = types.FSInputFile(path=giv_photo.path)
        if giv_obj.photo_id:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file_id=giv_obj.photo_id, file=photo)
            new_id, mes = await mw.try_send_photo(md=md)
            if new_id:
                await gs.update_giv_photo_id(giv_obj=giv_obj, photo_id=new_id)
        else:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file=photo)
            new_id, mes = await mw.try_send_photo(md=md)
            await gs.update_giv_photo_id(giv_obj=giv_obj, photo_id=new_id)
    elif giv_video:
        video = types.FSInputFile(path=giv_video.path)
        if giv_obj.video_id:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file_id=giv_obj.video_id, file=video)
            new_id, mes = await mw.try_send_video(md=md)
            if new_id:
                await gs.update_giv_video_id(giv_obj=giv_obj, video_id=new_id)
        else:
            md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard, file=video)
            new_id, mes = await mw.try_send_video(md=md)
            await gs.update_giv_video_id(giv_obj=giv_obj, video_id=new_id)    
    else:
        md = MessageData(text=giv_text, telegram_id=place_id, keyboard=keyboard)
        mes = await mw.try_send_message(md=md)
    mes_id = mes.message_id
    chat_id = str(mes.chat.id).replace("-100", "")
    link = f"https://t.me/c/{chat_id}/{mes_id}"
    await gs.create_giv_post(place_id=place_id, giv_obj=giv_obj, mes_id=mes_id, mes_link=link)





async def check_sub(telegram_id:str|int, channel_ids:list)-> bool | tuple:  
    TOKEN = getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    for chanel_id in channel_ids:
        try:
            status = await bot.get_chat_member(chat_id=chanel_id, user_id=telegram_id)
            if isinstance(status, types.ChatMemberBanned) or isinstance(status, types.ChatMemberLeft):
                return False
        except:
            return False
    return True