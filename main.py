from data.settings import bot, dp
from asyncio import run
from utils.notification import start, shutdown
import handlers

async def main():
    try:
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        await dp.start_polling(bot)
    finally:
        await bot.session().close()





if __name__=='__main__':
    run(main())


