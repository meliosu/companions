import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.handlers import router

import os

bot = Bot(os.environ['COMPANIONS_TG_TOKEN'])
dispatcher = Dispatcher()


async def main():
    dispatcher.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('cancelled')
