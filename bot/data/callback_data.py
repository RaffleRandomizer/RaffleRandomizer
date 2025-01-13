from aiogram.filters.callback_data import CallbackData

class Help(CallbackData, prefix="help"):
    lvl_1: int|None = None
    back: bool = False

class Orders(CallbackData, prefix="ord"):
    lvl_1: int|None = None
    ord_id: int|None = None
    req_id: int|None = None
    back: bool = False