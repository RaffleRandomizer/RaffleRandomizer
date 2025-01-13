from datetime import datetime, timedelta
from bot.config.loader import moscow_tz

async def get_dts():
    today = datetime.now().astimezone(moscow_tz)
    ten_min = today + timedelta(minutes=10)
    one_hour = today + timedelta(hours=1)
    one_day = today + timedelta(days=1)
    one_week = today + timedelta(weeks=1)
    dates = {
        "ten_min": f'`{ten_min.strftime("%d.%m.%Y %H:%M")}`',
        "one_hour": f'`{one_hour.strftime("%d.%m.%Y %H:%M")}`',
        "one_day": f'`{one_day.strftime("%d.%m.%Y %H:%M")}`',
        "one_week": f'`{one_week.strftime("%d.%m.%Y %H:%M")}`',
    }
    return dates

async def get_now_plus_one_minute():
    today = datetime.now().astimezone(moscow_tz)
    one_min = today + timedelta(minutes=1)
    return one_min.astimezone(moscow_tz)


def is_valid_datetime(date_time_str):
    try:
        # Попытка преобразовать строку в объект datetime
        datetime.strptime(date_time_str, '%d.%m.%Y %H:%M')
        return True
    except ValueError:
        return False
  

def is_future_datetime(date_time_str):
    try:
        # Попытка преобразовать строку в объект datetime
        dt = datetime.strptime(date_time_str, '%d.%m.%Y %H:%M').astimezone(moscow_tz)
        now = datetime.now().astimezone(moscow_tz)
        if dt > now:
            return True
        return False
    except ValueError:
        return False
    


def is_post_before_results_datetime(post_dt: datetime, results_dt: datetime):
    try:
        # Попытка преобразовать строку в объект datetime
        post_dt = post_dt.astimezone(moscow_tz)
        results_dt = results_dt.astimezone(moscow_tz)
        if results_dt > post_dt:
            return True
        return False
    except ValueError:
        return False
    


def get_datiteme_object(date:str):
    result = datetime.strptime(date, "%d.%m.%Y %H:%M")
    return result.astimezone(moscow_tz)

async def get_datetime_str(date:datetime):
    return date.strftime("%d.%m.%Y %H:%M")