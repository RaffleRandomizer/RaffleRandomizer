from aiogram import types, Router, filters, F
from aiogram.fsm.context import FSMContext
from telegram.services import telegram_user as tus
from bot.data import bot_data as td
from bot.data.dataclasses import MessageData
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.utils import message_worker as mw
from aiogram.utils.deep_linking import decode_payload
from bot_data.services import text as ts
from bot.config.loader import bot, moscow_tz
from telegram.models import TelegramUser
from pprint import pprint
from aiogram.enums import ChatMemberStatus
from randomizer.services import chat as cs
from bot.states.DefaultState import DefaultState
from bot.handlers.main_menu import check_cancel
from randomizer.services import givs as gs
from datetime import datetime
from randomizer.models import Giveaway
from bot.utils import giv as gp
from bot.utils import date_worker as dw
from bot.handlers.main_menu import my_channels, create_giv, my_givs, send_cancel
from aiogram.types import BotCommand

commands = Router()

@commands.message(filters.Command("set"))
async def set_bot_commands(message: types.Message, state: FSMContext, telegram_id:str):
    if str(telegram_id) == "390959255":
        commands = [
            BotCommand(command="start", description="Bot's menu | Меню бота"),
            BotCommand(command="new_lot", description="New giveaway | Новый розыгрыш"),
            BotCommand(command="my_lots", description="My giveaways | Ваши розыгрыши"),
            BotCommand(command="my_channels", description="My channels | Ваши каналы"),
        ]
        await bot.set_my_commands(commands)


@commands.message(filters.CommandStart())
async def command_start(message: types.Message,state: FSMContext, telegram_id:str):
    if "checklot" in message.text:
        text = await process_check_giv(message=message)
        md = MessageData(telegram_id=telegram_id, text=text, state=state)
        await mw.try_send_message(md)
        return
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True) or await tus.create_telegram_user(
        name=message.from_user.full_name,
        telegram_id=telegram_id,
        username=message.from_user.username,     
    )
    await check_cancel(state=state, telegram_id=telegram_id)
    await state.set_state(DefaultState.DEFAULT_STATE)
    await send_hello_message(message=message, state=state, user=user)


async def process_check_giv(message:types.Message):
    giv_uuid = message.text.replace("/start checklot", "")
    giv = await gs.get_giveaway_by_uuid(giv_uuid=giv_uuid)
    if giv:
        if giv.ended_by_creator:
            text = await ts.get_text_by_language_and_key(key=td.GIV_RESULTS_AUTOR, lang=giv.creator.selected_language)
        elif giv.giv_results_dt:
            text = await ts.get_text_by_language_and_key(key=td.GIV_RESULTS_DT, lang=giv.creator.selected_language)
        else:
            text = await ts.get_text_by_language_and_key(key=td.GIV_RESULTS_COUNT, lang=giv.creator.selected_language)

        giv_num = giv.pk
        parts_count = await gs.get_parts_count(giv_obj=giv)
        winners_count = giv.winners_count
        if giv.giv_results_dt:
            text = text.format(dt=await dw.get_datetime_str(giv.giv_results_dt.astimezone(moscow_tz)),
                               giv_num=giv_num, 
                               parts_count=parts_count, 
                               winers_count=winners_count)
        else:
            text = text.format(giv_num=giv_num, 
                               parts_count=parts_count, 
                               winers_count=winners_count) 
        winners = await gs.get_giv_winners(giv_obj=giv)
        result = "\n"
        for winner in winners[:winners_count]:
            place_and_name = f"{winner.place}. "
            if winner.winner.username:
                place_and_name += f"@{winner.winner.username}"
            else:
                place_and_name += f'<a href="tg://user?id={winner.winner.telegram_id}">{winner.winner.name}</a>'
            place_and_name += f" ({winner.winner.telegram_id})\n"
            result += place_and_name
        text += result
        return text



@commands.message(filters.Command("delete_channel"))
async def delete_channel(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    channel_id = message.text.split()[1]
    place = await cs.get_place(place_id=channel_id)
    if place:
        result = await cs.delete_admin_from_place(place=place, user=user)
        if result:
            text = await ts.get_text_by_language_and_key(key=td.CHANNEL_DELETED, lang=user.selected_language)
        else:
            text = await ts.get_text_by_language_and_key(key=td.NOT_ADMIN, lang=user.selected_language)
    else:
        text = await ts.get_text_by_language_and_key(key=td.NOT_ADMIN, lang=user.selected_language)
    md = MessageData(
        telegram_id=telegram_id,
        text=text,
        state=state,
    )
    await state.set_state(DefaultState.DEFAULT_STATE)
    await mw.try_send_message(md=md)

@commands.message(filters.Command("my_channels"))
async def call_my_channels(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    await my_channels(message=message, state=state, telegram_id=telegram_id)

@commands.message(filters.Command("new_lot"))
async def call_new_lot(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    await create_giv(message=message, state=state, telegram_id=telegram_id)

@commands.message(filters.Command("my_lots"))
async def call_my_lots(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    await my_givs(message=message, state=state, telegram_id=telegram_id)

@commands.message(filters.Command("cancel"))
async def call_my_lots(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    await send_cancel(state=state, telegram_id=telegram_id)

@commands.message(filters.Command("delete_lot"))
async def delete_lot(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = message.text.split()[1]
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    if giv:
        if giv.creator == user:
            if giv.deleted_by_creator:
                text = await ts.get_text_by_language_and_key(key=td.LOT_ALREADY_DELETED, lang=user.selected_language)
                md = MessageData(telegram_id=telegram_id, text=text, state=state)
                await mw.try_send_message(md=md)
                return
        
            now = datetime.now().astimezone(moscow_tz)
            if giv.post_giv_dt.astimezone(moscow_tz) > now:
                status = "waiting"
            elif giv.ended:
                status = "end"
            else:
                status = "public"
            if status == "waiting":
                text = await ts.get_text_by_language_and_key(key=td.WAITING_LOT_DELETED, lang=user.selected_language)
                await gs.update_giv_deleted(giv_obj=giv)
                md = MessageData(telegram_id=telegram_id, text=text, state=state)
                await mw.try_send_message(md=md)
            else:
                text = await ts.get_text_by_language_and_key(key=td.LOT_DELETED, lang=user.selected_language)
                await gs.update_giv_deleted(giv_obj=giv)
                post = await gs.get_giv_post_by_place_and_giveaway(place=giv.post_channels, giveaway=giv)
                text = text.format(link=post.message_link)
                md = MessageData(telegram_id=telegram_id, text=text, state=state)
                await mw.try_send_message(md=md)
        else:
            text = await ts.get_text_by_language_and_key(key=td.NOT_YOUR_GIV, lang=user.selected_language)
            md = MessageData(telegram_id=telegram_id, text=text, state=state)
            await mw.try_send_message(md=md)
    else:
        text = await ts.get_text_by_language_and_key(key=td.LOT_NOT_FOUND, lang=user.selected_language)
        md = MessageData(telegram_id=telegram_id, text=text, state=state)
        await mw.try_send_message(md=md)

@commands.message(F.text.startswith("/mylot"))
async def mylot(message: types.Message,state: FSMContext, telegram_id:str):
    await check_cancel(state=state, telegram_id=telegram_id)
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = message.text.replace("/mylot", "")
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    if giv:
        if giv.creator == user:
            post = await gs.get_giv_post_by_place_and_giveaway(place=giv.post_channels, giveaway=giv)
            link = post.message_link if post else False
            status = ""
            now = datetime.now().astimezone(moscow_tz)
            if giv.post_giv_dt.astimezone(moscow_tz) > now:
                status = "waiting"
            elif giv.ended:
                status = "end"
            else:
                status = "public"
            parts_count = await gs.get_parts_count(giv_obj=giv)
            winners_count = giv.winners_count

            if giv.giv_results_dt:
                text = await ts.get_text_by_language_and_key(key=td.LOT_DATA_DT, lang=user.selected_language)
                end_dt = giv.giv_results_dt.astimezone(moscow_tz)
                end_dt_str = await dw.get_datetime_str(date=end_dt)
                if link:
                    text = text.format(
                        pk=giv.pk,
                        link=link,
                        status=status,
                        parts_count=parts_count,
                        winners_count=winners_count,
                        end_dt=end_dt_str,
                    )
                else:
                    text = text.replace('<a href="{link}">Сообщение с розыгрышем</a>', "")
                    text = text.format(
                        pk=giv.pk,
                        status=status,
                        parts_count=parts_count,
                        winners_count=winners_count,
                        end_dt=end_dt_str,
                    )
            else:
                text = await ts.get_text_by_language_and_key(key=td.LOT_DATA_COUNT, lang=user.selected_language)
                if link:
                    text = text.format(
                        pk=giv.pk,
                        link=link,
                        status=status,
                        parts_count=parts_count,
                        winners_count=winners_count,
                        end_count=giv.giv_results_count,
                    )
                else:
                    text = text.replace('<a href="{link}">Сообщение с розыгрышем</a>', "")
                    text = text.format(
                        pk=giv.pk,
                        status=status,
                        parts_count=parts_count,
                        winners_count=winners_count,
                        end_count=giv.giv_results_count,
                    )
            keyboard = await ik.lot_kb(lang=user.selected_language, status=status, giv_pk=giv.pk)
            md = MessageData(telegram_id=telegram_id, text=text, state=state, keyboard=keyboard)
            await mw.try_send_message(md=md)
        else:
            text = await ts.get_text_by_language_and_key(key=td.NOT_YOUR_GIV, lang=user.selected_language)
            md = MessageData(telegram_id=telegram_id, text=text, state=state)
            await mw.try_send_message(md=md)
    else:
        text = await ts.get_text_by_language_and_key(key=td.LOT_NOT_FOUND, lang=user.selected_language)
        md = MessageData(telegram_id=telegram_id, text=text, state=state)
        await mw.try_send_message(md=md)


@commands.message(F.text.startswith("/postlot"))
async def postlot(message: types.Message,state: FSMContext, telegram_id:str):
    print(1232)
    await check_cancel(state=state, telegram_id=telegram_id)
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_uuid = message.text.replace("/postlot", "")
    giv = await gs.get_giveaway_by_uuid(giv_uuid=giv_uuid)
    if giv:
        now = datetime.now().astimezone(moscow_tz)
        if giv.post_giv_dt.astimezone(moscow_tz) > now or giv.ended:
            text = await ts.get_text_by_language_and_key(key=td.GIV_ENDED_OR_NOT_POSTED_POSTLOT, lang=user.selected_language)
            md = MessageData(telegram_id=telegram_id, text=text, state=state)
            await mw.try_send_message(md=md)
        else:
            await send_giv_example(giv_obj=giv, state=state, telegram_id=telegram_id)
            text = await ts.get_text_by_language_and_key(key=td.ADD_CHANNELS_TO_PUB, lang=user.selected_language)
            user_channels = await tus.get_user_places(telegram_id=telegram_id)
            keyboard = await ik.giv_user_channels_post_now(user_channels_list=user_channels, giv_pk=giv.pk)
            md = MessageData(text=text, state=state, telegram_id=telegram_id, keyboard=keyboard)
            await mw.try_send_message(md=md)
    else:
        text = await ts.get_text_by_language_and_key(key=td.LOT_NOT_FOUND, lang=user.selected_language)
        md = MessageData(text=text, state=state, telegram_id=telegram_id)
        await mw.try_send_message(md=md)

async def send_giv_example(giv_obj:Giveaway, state: FSMContext, telegram_id:str):
    giv_text = giv_obj.giv_text
    giv_photo = giv_obj.photo
    giv_video = giv_obj.video
    parts = await gs.get_parts_count(giv_obj=giv_obj)
    btn_text = f"{giv_obj.button_type_text} ({parts})"
    keyboard = await ik.get_giv_kb(kb_text=btn_text)
    if giv_photo:
        if giv_obj.photo_id:
            photo = types.FSInputFile(path=giv_photo.path)
            md = MessageData(text=giv_text, state=state, telegram_id=telegram_id, keyboard=keyboard, file_id=giv_obj.photo_id, file=photo)
            new_id, mes = await mw.try_send_photo(md=md)
            if new_id:
                await gs.update_giv_photo_id(giv_obj=giv_obj, photo_id=new_id)
        else:
            photo = types.FSInputFile(path=giv_photo.path)
            md = MessageData(text=giv_text, state=state, telegram_id=telegram_id, keyboard=keyboard, file=photo)
            new_id, mes = await mw.try_send_photo(md=md)
            await gs.update_giv_photo_id(giv_obj=giv_obj, photo_id=new_id)
    elif giv_video:
        video = types.FSInputFile(path=giv_video.path)
        if giv_obj.video_id:
            md = MessageData(text=giv_text, state=state, telegram_id=telegram_id, keyboard=keyboard, file_id=giv_obj.video_id, file=video)
            new_id, mes = await mw.try_send_video(md=md)
            if new_id:
                await gs.update_giv_video_id(giv_obj=giv_obj, video_id=new_id)
        else:
            md = MessageData(text=giv_text, state=state, telegram_id=telegram_id, keyboard=keyboard, file=video)
            new_id, mes = await mw.try_send_video(md=md)
            await gs.update_giv_video_id(giv_obj=giv_obj, video_id=new_id)
    else:
        md = MessageData(text=giv_text, state=state, telegram_id=telegram_id, keyboard=keyboard)
        await mw.try_send_message(md=md)


async def send_hello_message(message: types.Message, state: FSMContext, user:TelegramUser):
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

@commands.my_chat_member()
async def test_chat_member(chat_member: types.ChatMemberUpdated):
    user = await tus.get_user_by_id(telegram_id=chat_member.from_user.id)
    status = chat_member.new_chat_member.status
    me = await bot.me()
    if user and chat_member.chat.type == "private":
        if status == ChatMemberStatus.KICKED:
            await tus.update_user_blocked_bot(block=True, user=user)
        elif status == ChatMemberStatus.MEMBER:
            await tus.update_user_blocked_bot(block=False, user=user)
    elif chat_member.chat.type != "private":
        if not user:
            user = await tus.create_telegram_user(
                name=chat_member.from_user.full_name,
                telegram_id=chat_member.from_user.id,
                username=chat_member.from_user.username
            )
        if chat_member.new_chat_member.user.id == me.id:
            title = chat_member.chat.title
            place_type = chat_member.chat.type
            place_id = chat_member.chat.id
            username = chat_member.chat.username
            place = await cs.get_place(place_id=place_id)
            if status == ChatMemberStatus.ADMINISTRATOR:
                if not place:
                    await cs.create_place(
                        title=title,
                        place_type=place_type,
                        place_id=place_id,
                        admin_rights=True,
                        username=username,
                    )
                elif not place.admin_rights:
                    await cs.update_place_admin_rights(place_id=place_id, admin_rights=True)
                    print("rights_updated")
                await cs.update_place_admins(place_id=place_id, admins_list=[user])
            elif status in [ChatMemberStatus.KICKED, ChatMemberStatus.LEFT]:
                await cs.delete_place(place_id=place_id)
            elif status == ChatMemberStatus.MEMBER:
                await cs.create_place(
                    title=title,
                    place_type=place_type,
                    place_id=place_id,
                    admin_rights=False,
                    username=username,
                )
            
            
@commands.message(F.content_type == types.ContentType.MIGRATE_TO_CHAT_ID)
async def migrate_event(message: types.Message):
    if message.migrate_to_chat_id:
        old_id, new_id = message.chat.id, message.migrate_to_chat_id
        await cs.update_place_id(place_id=old_id, new_id=new_id)