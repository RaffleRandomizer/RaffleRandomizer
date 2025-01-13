from telegram.models import TelegramUser
from bot_data.services import text as txt

async def create_telegram_user(name:str, telegram_id:int, username:str = None):
    language = await txt.get_default_language()
    user = await TelegramUser.objects.acreate(
        name=name,
        telegram_id=telegram_id,
        username=username,
        selected_language=language,
    )
    return user



async def get_all_users():
    users = []
    async for user in TelegramUser.objects.filter():
        users.append(user)
    return users



async def get_user_by_id(telegram_id: int, lang:bool = False):
    if lang:
        user = await TelegramUser.objects.filter(telegram_id=telegram_id).select_related("selected_language").afirst()
    else:
        user = await TelegramUser.objects.filter(telegram_id=telegram_id).afirst()
    return user

async def update_user_blocked_bot(block:bool, user:TelegramUser):
    user.bot_blocked = block
    await user.asave()
    return user

async def update_user_language(user:TelegramUser):
    lang = user.selected_language
    if lang.name == "Русский язык":
        user.selected_language = await txt.get_language_by_name("Английский язык")
    else:
        user.selected_language = await txt.get_language_by_name("Русский язык")
    await user.asave()
    return user


async def get_user_places(telegram_id: int|str):
    user = await TelegramUser.objects.filter(telegram_id=telegram_id).prefetch_related("chats").afirst()
    places = []
    async for place in user.chats.filter():
        places.append(place)
    return places
