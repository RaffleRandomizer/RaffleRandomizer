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
from randomizer.services import givs as gs
from datetime import datetime
from aiogram.enums import ParseMode
from bot.config.loader import moscow_tz
from bot.utils import date_worker as dw
from bot.utils import giv as gp
from aiogram.utils.deep_linking import create_start_link
from randomizer_bot.settings import BASE_DIR
import os
import csv

lot_actions = Router()

@lot_actions.callback_query(F.data.startswith(td.IK_CHANGE_COND))
async def change_cond(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    now = datetime.now().astimezone(moscow_tz)
    if giv.post_giv_dt.astimezone(moscow_tz) > now:
        status = "waiting"
    elif giv.ended:
        status = "end"
    else:
        status = "public"
    if status == "end":
        return
    await state.update_data({"selected_giv":giv_pk})
    await call.answer()
    text = await ts.get_text_by_language_and_key(key=td.GIV_HOW_TO_END, lang=user.selected_language)
    keyboard = await ik.edit_lot_cond(lang=user.selected_language)
    await state.set_state(DefaultState.GIV_HOW_TO_END)
    md = MessageData(text=text, telegram_id=telegram_id, keyboard=keyboard, state=state)
    await mw.try_send_message(md)

@lot_actions.callback_query(F.data.startswith(td.IK_DEL_LOT))
async def delete_lot(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    await call.answer()
    text = await ts.get_text_by_language_and_key(key=td.DELETE_LOT, lang=user.selected_language)
    text = text.format(pk=giv_pk)
    md = MessageData(text=text, telegram_id=telegram_id, state=state, parse_mode=ParseMode.MARKDOWN_V2)
    await mw.try_send_message(md)

@lot_actions.callback_query(F.data == td.IK_BCU, filters.StateFilter(DefaultState.GIV_HOW_TO_END))
async def change_end_by_count(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    print("call change_end_by_count") 
    await call.answer()
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.WHEN_END_COUNT, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md)
    await state.set_state(DefaultState.LOT_COUNT_WAIT)

@lot_actions.callback_query(F.data == td.IK_EBT, filters.StateFilter(DefaultState.GIV_HOW_TO_END))
async def change_end_dt(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    await call.answer()
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text_1 = await ts.get_text_by_language_and_key(key=td.WHEN_END_DT, lang=user.selected_language)
    text_examples = await ts.get_text_by_language_and_key(key=td.GIV_TD_EXAMPLES, lang=user.selected_language)
    dates = await dw.get_dts()
    text_examples = text_examples.format(**dates)
    md_1 = MessageData(text=text_1, telegram_id=telegram_id, state=state)
    md_2 = MessageData(text=text_examples, telegram_id=telegram_id, state=state, parse_mode=ParseMode.MARKDOWN_V2)
    await mw.try_send_message(md_1)
    await mw.try_send_message(md_2)
    await state.set_state(DefaultState.LOT_DT_WAIT)


@lot_actions.message(F.text, filters.StateFilter(DefaultState.LOT_DT_WAIT))
async def check_is_date_correct(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True) 
    dt = message.text
    is_valid = dw.is_valid_datetime(date_time_str=dt)
    if is_valid:
        if dw.is_future_datetime(date_time_str=dt):
            key = td.GIV_DT_SELECT_WINNER
            data = await state.get_data()
            selected_giv = data.get("selected_giv", None)
            if selected_giv:
                date = dw.get_datiteme_object(date=dt)
                giv = await gs.get_giveaway_by_pk(giv_pk=selected_giv)
                if dw.is_post_before_results_datetime(results_dt=date, post_dt=giv.post_giv_dt):
                    await gs.update_giv_end_dt(giv_obj=giv, date=date)
                    await state.set_state(DefaultState.DEFAULT_STATE)
                else:
                    key = td.GIV_POST_BEFORE_RESULTS
        else:
            key = td.GIV_DT_NOT_FUTURE
    else:
        key = td.GIV_WRONG_DT_FORMAT
    
    text = await ts.get_text_by_language_and_key(key=key, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md=md)
    


@lot_actions.message(F.text, filters.StateFilter(DefaultState.LOT_COUNT_WAIT))
async def lot_waiting_count_users(message: types.Message, state: FSMContext, telegram_id:str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    try:
        users_count = int(message.text)
        data = await state.get_data()
        if users_count < 0:
            users_count *= -1
        selected_giv = data.get("selected_giv", None)
        if selected_giv: 
            giv = await gs.get_giveaway_by_pk(giv_pk=selected_giv)
            if users_count < giv.winners_count:
                text = await ts.get_text_by_language_and_key(key=td.GIV_PARTS_LESS_THAN_WINNERS, lang=user.selected_language)
                md = MessageData(text=text, telegram_id=telegram_id, state=state)
                await mw.try_send_message(md=md)
                return
            await gs.update_giv_end_count(giv_obj=giv, count=users_count)
        text = await ts.get_text_by_language_and_key(key=td.GIV_END_USERS_COUNT, lang=user.selected_language)
        text = text.format(count=users_count)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md=md)
        await state.set_state(DefaultState.DEFAULT_STATE)
    except Exception as e:
        print(e)
        text = await ts.get_text_by_language_and_key(key=td.NEED_NUMBER, lang=user.selected_language)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md=md)
        return


@lot_actions.callback_query(F.data.startswith(td.IK_END_GIV_CANCEL))
async def cancel_end(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    await call.message.delete()

@lot_actions.callback_query(F.data.startswith(td.IK_GET_LINK))
async def get_link(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    text = await ts.get_text_by_language_and_key(key=td.CHECK_LINK, lang=user.selected_language)
    check_link = await create_start_link(bot=bot, payload=f"checklot{giv.unique_id}")
    text = text.format(link=check_link)
    md = MessageData(telegram_id=telegram_id, text=text, state=state, parse_mode=ParseMode.MARKDOWN_V2) 
    await mw.try_send_message(md=md) 
    await call.answer()



@lot_actions.callback_query(F.data.startswith(td.IK_END_GIV))
async def end_lot(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    await call.answer()
    text = await ts.get_text_by_language_and_key(key=td.CANT_END_GIV, lang=user.selected_language)
    md = MessageData(text=text, telegram_id=telegram_id, state=state)
    await mw.try_send_message(md)


@lot_actions.callback_query(F.data.startswith(td.IK_ADD_WINNERS))
async def add_new_winners(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    await call.answer()
    if giv and giv.ended:
        text = await ts.get_text_by_language_and_key(key=td.SELECT_NEW_WINNERS, lang=user.selected_language)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md)
        await state.set_state(DefaultState.NEW_WINNERS_COUNT_WAIT)
        await state.update_data({"current_giv_pk":giv_pk})
        

@lot_actions.message(F.text and filters.StateFilter(DefaultState.NEW_WINNERS_COUNT_WAIT))
async def get_count_new_winners(message:types.Message, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    n = message.text
    try:
        n = int(n)
        if n < 0:
            n*=-1
        data = await state.get_data()
        current_giv_pk = data.get("current_giv_pk", None)
        if current_giv_pk:
            giv = await gs.get_giveaway_by_pk(giv_pk=current_giv_pk)
            if giv:
                help = await ts.get_text_by_language_and_key(key=td.HELP_GIV_RESULTS, lang=user.selected_language)
                md = MessageData(text=help, telegram_id=telegram_id, state=state)
                await mw.try_send_message(md)
                ended = await ts.get_text_by_language_and_key(key=td.RE_SELECT_ENDED, lang=user.selected_language)
                md = MessageData(text=ended, telegram_id=telegram_id, state=state)
                await mw.try_send_message(md)
        else:
            raise Exception("Почемуто giv pk не засейвлен")

    except:
        text = await ts.get_text_by_language_and_key(key=td.NEED_NUMBER, lang=user.selected_language)
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md)
        return


@lot_actions.callback_query(F.data.startswith(td.IK_END_NOW))
async def end_applied(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    await call.answer()
    text = await ts.get_text_by_language_and_key(key=td.APPLY_END, lang=user.selected_language)
    keyboard = await ik.end_giv_now_or_not(lang=user.selected_language, giv_pk=giv_pk)
    md = MessageData(text=text, telegram_id=telegram_id, state=state, keyboard=keyboard)
    await mw.try_send_message(md)




@lot_actions.callback_query(F.data.startswith(td.IK_GET_EXCEL))
async def end_applied(call: types.CallbackQuery, state: FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = call.data.split("_")[-1]
    await call.answer()
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    if giv:
        giv_parts_count = await gs.get_parts_count(giv_obj=giv)
        text = await ts.get_text_by_language_and_key(key=td.GET_TABLE_START, lang=user.selected_language)
        text = text.format(pk=giv_pk, parts_count=giv_parts_count, price="нужен тариф для подсчета звезд")
        md = MessageData(text=text, telegram_id=telegram_id, state=state)
        await mw.try_send_message(md)
        title = await ts.get_text_by_language_and_key(key=td.PAYMENT_HEAD, lang=user.selected_language)
        title = title.format(pk=giv_pk)
        body = await ts.get_text_by_language_and_key(key=td.PAYMENT_BODY, lang=user.selected_language)
        body = body.format(count=giv_parts_count)
        stars_count = await gs.get_price(lines_count=giv_parts_count)
        prices = [types.LabeledPrice(label="XTR", amount=stars_count)]  
        await bot.send_invoice(  
            chat_id=telegram_id,
            title=title,  
            description=body,  
            prices=prices,  
            provider_token="",  
            payload=f"giv_{giv_pk}",  
            currency="XTR",   
        )

@lot_actions.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: types.PreCheckoutQuery):  
    await pre_checkout_query.answer(ok=True)

@lot_actions.message(F.successful_payment)
async def success_payment_handler(message: types.Message, state:FSMContext, telegram_id: str):
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    giv_pk = message.successful_payment.invoice_payload.split("_")[-1]
    giv = await gs.get_giveaway_by_pk(giv_pk=giv_pk)
    if giv:
        giv_parts_count = await gs.get_parts_count(giv_obj=giv)
        parts = await gs.get_parts(giv_obj=giv)
        filename = f"{giv.unique_id}.csv"
        path = os.path.join(BASE_DIR, "temp", filename)
        with open(path,"w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Имя Фамилия', 'username'])
            for part in parts:
                writer.writerow([part.telegram_id, part.name, part.username if part.username else "username отсутствует"])
        text = await ts.get_text_by_language_and_key(key=td.CSV_DATA, lang=user.selected_language)
        text = text.format(giv_pk=giv_pk, lines_count=giv_parts_count)
        try:
            await bot.send_document(chat_id=telegram_id, document=types.FSInputFile(path=path), caption=text )
        except Exception as e:
            print(e)
        os.remove(path)
    


@lot_actions.message()
async def random_message(message: types.Message, state: FSMContext, telegram_id:str):
    pprint(message.model_dump())
    user = await tus.get_user_by_id(telegram_id=telegram_id, lang=True)
    text = await ts.get_text_by_language_and_key(key=td.DEFAULT_MESSAGE, lang=user.selected_language)
    await message.answer(text=text, parse_mode=ParseMode.HTML)
