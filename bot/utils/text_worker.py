
# from logistic_system.models import Order
# from typing import List
# from bot.config.loader import moscow_tz


# async def get_orders_text(orders: List[Order]) -> str:
#     text = ""
#     strf = "%d.%m.%Y %H:%M"
#     for index, order in enumerate(orders):
#         start_time = order.start_datetime.astimezone(moscow_tz)
#         dt = start_time.strftime(strf)
#         text += f"{index + 1}) {order.cargo} - {dt}\n"
#     return text

# async def get_order_date(order:Order) -> str:
#     end_time = order.start_datetime.astimezone(moscow_tz)
#     return await date_formater(end_time)

# async def date_formater(datetime_obj):
#     strf = "%d.%m.%Y %H:%M"
#     dt = datetime_obj.astimezone(moscow_tz).strftime(strf)
#     return dt