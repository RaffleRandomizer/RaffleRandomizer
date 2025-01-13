from aiogram import types
from aiogram.fsm.context import FSMContext
from bot.data.dataclasses import MessageData
import logging
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from bot.config.loader import bot
from bot.keyboards import inline as ik
import traceback
from aiogram.types.link_preview_options import LinkPreviewOptions
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from os import getenv

async def try_send_message(md: MessageData): 
    try:
        if md.reply_to_message_id:
            try:
                mes = await bot.send_message(
                    chat_id=md.telegram_id,
                    text=md.text,
                    reply_markup=md.keyboard,
                    parse_mode=md.parse_mode,
                    reply_to_message_id=md.reply_to_message_id,
                    link_preview_options=LinkPreviewOptions(is_disabled=True)
                )
            except:
                mes = await bot.send_message(
                    chat_id=md.telegram_id,
                    text=md.text,
                    reply_markup=md.keyboard,
                    parse_mode=md.parse_mode,
                    link_preview_options=LinkPreviewOptions(is_disabled=True)
                )
        else:
            mes = await bot.send_message(
                chat_id=md.telegram_id,
                text=md.text,
                reply_markup=md.keyboard,
                parse_mode=md.parse_mode,
                link_preview_options=LinkPreviewOptions(is_disabled=True)
            )
        if md.delete_previous_main_mesage and md.state:
            data = await md.state.get_data()
            await try_delete_message(
                chat_id=md.telegram_id,
                message_id=data.get("main_message_id")
            )
        if md.main_message and md.state:
            await md.state.update_data(
                {
                    "main_message_id": mes.message_id
                }
            )
            print("new main_message", mes.message_id)
        if md.clear_delete_list and md.state:
            data = await md.state.get_data()
            delete_list = data.get("delete_list", [])
            for message_id in delete_list:
                await try_delete_message(message_id=message_id, chat_id=md.telegram_id)
        return mes
    except Exception as e:
        logging.exception(e)
        TOKEN = getenv("BOT_TOKEN")
        new_bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        try:
            if md.reply_to_message_id:
                try:
                    mes = await new_bot.send_message(
                        chat_id=md.telegram_id,
                        text=md.text,
                        reply_markup=md.keyboard,
                        parse_mode=md.parse_mode,
                        reply_to_message_id=md.reply_to_message_id,
                        link_preview_options=LinkPreviewOptions(is_disabled=True)
                    )
                except:
                    mes = await new_bot.send_message(
                        chat_id=md.telegram_id,
                        text=md.text,
                        reply_markup=md.keyboard,
                        parse_mode=md.parse_mode,
                        link_preview_options=LinkPreviewOptions(is_disabled=True)
                    )
            else:
                mes = await new_bot.send_message(
                    chat_id=md.telegram_id,
                    text=md.text,
                    reply_markup=md.keyboard,
                    parse_mode=md.parse_mode,
                    link_preview_options=LinkPreviewOptions(is_disabled=True)
                )
            if md.delete_previous_main_mesage and md.state:
                data = await md.state.get_data()
                await try_delete_message(
                    chat_id=md.telegram_id,
                    message_id=data.get("main_message_id")
                )
            if md.main_message and md.state:
                await md.state.update_data(
                    {
                        "main_message_id": mes.message_id
                    }
                )
                print("new main_message", mes.message_id)
            if md.clear_delete_list and md.state:
                data = await md.state.get_data()
                delete_list = data.get("delete_list", [])
                for message_id in delete_list:
                    await try_delete_message(message_id=message_id, chat_id=md.telegram_id)
            return mes
        except Exception as e:
            logging.exception(e)


async def try_send_photo(md: MessageData): 
    try:
        data = await md.state.get_data() if md.state else None
        new_id_flag = False
        new_id = None
        if md.file_id is not None:
            try:
                mes = await bot.send_photo(
                    photo=md.file_id,
                    chat_id=md.telegram_id,
                    caption=md.text,
                    reply_markup=md.keyboard
                )
            except:
                print("wrong file_id")
                mes = await bot.send_photo(
                    photo=md.file,
                    chat_id=md.telegram_id,
                    caption=md.text,
                    reply_markup=md.keyboard
                )
                new_id_flag = True
                new_id = mes.photo[-1].file_id
            
        else:    
            mes = await bot.send_photo(
                photo=md.file,
                chat_id=md.telegram_id,
                caption=md.text,
                reply_markup=md.keyboard
            )
            new_id_flag = True
            new_id = mes.photo[-1].file_id
        if md.delete_previous_main_mesage:
            await try_delete_message(
                chat_id=md.telegram_id,
                message_id=data.get("main_message_id")
            )

        if md.main_message and data:
            await md.state.update_data(
                {
                    "main_message_id": mes.message_id
                }
            )
            print("new main_message", mes.message_id)
        if md.add_to_delete_list and data:
            delete_list = data.get("delete_list", [])
            delete_list.append(mes.message_id)
            await md.state.update_data(
                {
                    "delete_list": delete_list
                }
            )
        return (new_id if new_id_flag else False), mes

    except Exception as e:
        logging.exception(e)
        TOKEN = getenv("BOT_TOKEN")
        new_bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        try:
            data = await md.state.get_data() if md.state else None
            new_id_flag = False
            new_id = None
            if md.file_id is not None:
                try:
                    mes = await new_bot.send_photo(
                        photo=md.file_id,
                        chat_id=md.telegram_id,
                        caption=md.text,
                        reply_markup=md.keyboard
                    )
                except:
                    print("wrong file_id")
                    mes = await new_bot.send_photo(
                        photo=md.file,
                        chat_id=md.telegram_id,
                        caption=md.text,
                        reply_markup=md.keyboard
                    )
                    new_id_flag = True
                    new_id = mes.photo[-1].file_id
                
            else:    
                mes = await new_bot.send_photo(
                    photo=md.file,
                    chat_id=md.telegram_id,
                    caption=md.text,
                    reply_markup=md.keyboard
                )
                new_id_flag = True
                new_id = mes.photo[-1].file_id
            if md.delete_previous_main_mesage:
                await try_delete_message(
                    chat_id=md.telegram_id,
                    message_id=data.get("main_message_id")
                )

            if md.main_message and data:
                await md.state.update_data(
                    {
                        "main_message_id": mes.message_id
                    }
                )
                print("new main_message", mes.message_id)
            if md.add_to_delete_list and data:
                delete_list = data.get("delete_list", [])
                delete_list.append(mes.message_id)
                await md.state.update_data(
                    {
                        "delete_list": delete_list
                    }
                )
            return (new_id if new_id_flag else False), mes

        except Exception as e:
            logging.exception(e)

async def try_send_video(md: MessageData): 
    try:
        data = await md.state.get_data() if md.state else None
        new_id_flag = False
        new_id = None
        if md.file_id is not None:
            try:
                mes = await bot.send_video(
                    video=md.file_id,
                    chat_id=md.telegram_id,
                    caption=md.text,
                    reply_markup=md.keyboard
                )
            except:
                mes = await bot.send_video(
                    video=md.file,
                    chat_id=md.telegram_id,
                    caption=md.text,
                    reply_markup=md.keyboard
                )
                new_id_flag = True
                new_id = mes.video.file_id 
        else:    
            mes = await bot.send_video(
                video=md.file,
                chat_id=md.telegram_id,
                caption=md.text,
                reply_markup=md.keyboard
            )
            new_id_flag = True
            new_id = mes.video.file_id
        if md.delete_previous_main_mesage:
            await try_delete_message(
                chat_id=md.telegram_id,
                message_id=data.get("main_message_id")
            )

        if md.main_message and data:
            await md.state.update_data(
                {
                    "main_message_id": mes.message_id
                }
            )
            print("new main_message", mes.message_id)
        if md.add_to_delete_list and data:
            delete_list = data.get("delete_list", [])
            delete_list.append(mes.message_id)
            await md.state.update_data(
                {
                    "delete_list": delete_list
                }
            )
        return (new_id if new_id_flag else False), mes

    except Exception as e:
        print(1111111)
        logging.exception(e)
        TOKEN = getenv("BOT_TOKEN")
        new_bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        try:
            data = await md.state.get_data() if md.state else None
            new_id_flag = False
            new_id = None
            if md.file_id is not None:
                try:
                    mes = await new_bot.send_video(
                        video=md.file_id,
                        chat_id=md.telegram_id,
                        caption=md.text,
                        reply_markup=md.keyboard
                    )
                except:
                    mes = await new_bot.send_video(
                        video=md.file,
                        chat_id=md.telegram_id,
                        caption=md.text,
                        reply_markup=md.keyboard
                    )
                    new_id_flag = True
                    new_id = mes.video.file_id 
            else:    
                mes = await new_bot.send_video(
                    video=md.file,
                    chat_id=md.telegram_id,
                    caption=md.text,
                    reply_markup=md.keyboard
                )
                new_id_flag = True
                new_id = mes.video.file_id
            if md.delete_previous_main_mesage:
                await try_delete_message(
                    chat_id=md.telegram_id,
                    message_id=data.get("main_message_id")
                )

            if md.main_message and data:
                await md.state.update_data(
                    {
                        "main_message_id": mes.message_id
                    }
                )
                print("new main_message", mes.message_id)
            if md.add_to_delete_list and data:
                delete_list = data.get("delete_list", [])
                delete_list.append(mes.message_id)
                await md.state.update_data(
                    {
                        "delete_list": delete_list
                    }
                )
            return (new_id if new_id_flag else False), mes

        except Exception as e:
            print(1111111)
            logging.exception(e)




async def try_edit_caption(md:MessageData):
    data = await md.state.get_data()
    try:
        await bot.edit_message_caption(
            caption=md.text,
            reply_markup=md.keyboard,
            chat_id=md.telegram_id,
            message_id=data.get("main_message_id")
        )
    except TelegramBadRequest:
        await try_delete_message(
            chat_id=md.telegram_id,
            message_id=data.get("main_message_id")
        )
        md.delete_previous_main_mesage = True
        await try_send_photo(md=md)


async def try_edit_main_message(md:MessageData):
    data = await md.state.get_data()
    try:
        await bot.edit_message_text(
            text=md.text,
            reply_markup=md.keyboard,
            chat_id=md.telegram_id,
            message_id=data.get("main_message_id"),
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )
    except Exception as e:
        if md.delete_on_edit:
            await try_delete_message(
                chat_id=md.telegram_id,
                message_id=data.get("main_message_id")
            )
            await try_send_message(md=md)

async def try_edit_this_message(md:MessageData):
    try:
        await bot.edit_message_text(
            text=md.text,
            reply_markup=md.keyboard,
            chat_id=md.telegram_id,
            message_id=md.this_message_id,
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )
        await md.state.update_data({
            "main_message_id":md.this_message_id
        })
    except TelegramBadRequest as e:
        print(e)
        if md.delete_on_edit:
            await try_delete_message(
                chat_id=md.telegram_id,
                message_id=md.this_message_id
            )
            await try_send_message(md=md)
    except Exception as e:
        pass




async def try_delete_message(message_id:int, chat_id:int):
    try:
        if message_id:
            await bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
    except TelegramBadRequest:
        logging.info(f"Can't delete main message from {chat_id}")
    except Exception as e:
        logging.exception(e)
    

async def _spamer(chat_id: int, text: str, keyboard,bot:Bot, photo:types.FSInputFile = None, video: types.FSInputFile = None ):
    if chat_id:
        if photo:
            try:
                await bot.send_photo(chat_id, photo, caption=text, reply_markup=keyboard, )
            except:
                logging.error(traceback.format_exc())
        elif video:
            try:
                await bot.send_video(chat_id, video, caption=text, reply_markup=keyboard)
            except:
                logging.error(traceback.format_exc())
        else:
            try:
                await bot.send_message(chat_id, text, reply_markup=keyboard, link_preview_options=LinkPreviewOptions(is_disabled=True))
            except:
                logging.error(traceback.format_exc())


async def spam_machine(text, chats, photo:types.FSInputFile = None, video: types.FSInputFile = None):
    keyboard = None
    TOKEN = getenv("BOT_TOKEN")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    async for chat in chats:
        if chat.telegram_user:
            await _spamer(chat_id=chat.telegram_user.telegram_id, text=text, keyboard=keyboard, photo=photo, video=video, bot=bot)