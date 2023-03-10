from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduler.parse_tasks import start_parse
from sqlalchemy.orm import sessionmaker
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from db.models import BaseModel
import os


async def on_startup(application):
    import handlers
    engine = create_async_engine(
        os.getenv('DB_URL', ''),
        future=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    dp['sessionmaker'] = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )


async def on_shutdown(application):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    bot = Bot(token=os.getenv('BOT_TOKEN', ''), parse_mode=ParseMode.HTML)

    dp = Dispatcher(bot, storage=MemoryStorage())
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        start_parse,
        'interval',
        hours=1,
        args=(dp, ),
    )

    scheduler.start()
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup, on_shutdown=on_shutdown)
