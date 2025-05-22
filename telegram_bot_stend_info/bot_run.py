import asyncio
import os
import asyncpg

from aiogram import Bot, Dispatcher
from handlers import router

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

    async def log_status(self, status_code, status_desc, stand):
        async with self.pool.acquire() as conn:
            await conn.execute('''INSERT INTO status(status_code, status_desc, stand) VALUES ($1, $2, $3)''', ...)

    async def log_version(self, stand, version):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO version(Stand, Version) 
                VALUES ($1, $2)
            ''', stand, version)

db = Database()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



async def main():
    await db.connect()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот был остановлен!')