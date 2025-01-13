from aiogram import BaseMiddleware
from aiogram import types

class DefaultMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler,
                       event: types.TelegramObject,
                       data):
        match type(event):
            case types.CallbackQuery:
                pass
            case types.Message:
                pass
            case _:
                await handler(event, data)
                return    
        telegram_id = event.from_user.id
        data["telegram_id"] = telegram_id
        await handler(event, data)
