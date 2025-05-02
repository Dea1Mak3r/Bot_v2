import asyncio
import os


from aiogram import Bot, Dispatcher
from data import BOT_TOKEN
from handlers import router

# env_path = '../.env'
# if os.path.exists(env_path):
#     with open(env_path, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if line and not line.startswith('#'):
#                 key, value = line.split('=', 1)
#                 os.environ[key] = value
#                 print(os.environ[key])
#
# # TOKEN = os.getenv('BOT_TOKEN')
# TOKEN = os.environ['BOT_TOKEN']

# if not TOKEN:
#     raise ValueError("Токен бота не установлен. Убедитесь, что переменная окружения BOT_TOKEN задана.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()



async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот был остановлен!')