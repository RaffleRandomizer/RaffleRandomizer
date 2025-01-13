from bot_data.models import Text, Language, Translate


async def get_text_by_language_and_key(lang: Language, key: str) -> str:
    if key is None:
        return "Нет текста"
    print("get_text_by_language_and_key", key)
    text_key = await Text.objects.filter(key=key).afirst()
    res = await Translate.objects.filter(text_key=text_key, language=lang).afirst()
    return res.translate


def get_text_by_language_and_key_sync(lang: Language, key: str) -> str:
    if key is None:
        return "Нет текста"
    print("get_text_by_language_and_key", key)
    text_key = Text.objects.filter(key=key).first()
    res = Translate.objects.filter(text_key=text_key, language=lang).first()
    return res.translate

async def get_default_language():
    return await Language.objects.afirst()

async def get_english_language():
    return await Language.objects.filter(name="Английский язык").afirst()

async def get_russian_language():
    return await Language.objects.filter(name="Русский язык").afirst()



def get_default_language_sync():
    return Language.objects.first()

async def get_language_by_name(lang_name: str) -> Language:
    return await Language.objects.filter(name=lang_name).afirst()

async def get_all_languages():
    languages = []
    async for lang in Language.objects.filter():
        languages.append(lang)
    return languages


async def get_text_by_key(key: str):
    text = await Text.objects.filter(key=key).afirst()
    return text.text if text else f"Ключ {key} отсутствует"

async def get_key_by_text(text: str):
    r = await Translate.objects.filter(translate=text).select_related("text_key").afirst()
    result = "1"
    if r:
        result = r.text_key.key
    return result

def get_key_by_text_sync(text: str):
    r = Translate.objects.filter(translate=text).select_related("text_key").first()
    result = "1"
    if r:
        result = r.text_key.key
    return result

def get_text_by_key_sync(key: str):
    text = Text.objects.filter(key=key).first()
    return text.text if text else f"Ключ {key} отсутствует"


