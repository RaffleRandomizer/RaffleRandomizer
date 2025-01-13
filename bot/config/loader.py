import logging
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import pytz
from aiogram.fsm.storage.redis import RedisStorage




TOKEN = getenv("BOT_TOKEN")
storage = RedisStorage.from_url(getenv("REDIS_URL"))
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
moscow_tz = pytz.timezone('Europe/Moscow')
logging.basicConfig(filename="bot_logs.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S %d.%m',
                    level=logging.DEBUG,
                    encoding="UTF-8")



# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())