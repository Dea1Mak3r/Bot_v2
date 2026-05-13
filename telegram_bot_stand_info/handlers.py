from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from bot_keyboard import main_keyboard, get_stand_choice_kb
from config import settings
import httpx

router = Router()
API_URL = settings.API_URL


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Приветствую!'
                         '\nДанный бот предоставляет возможности по получению информации о состоянии стендов.'
                         '\nНажмите /help чтобы получить информацию о доступных возможностях', reply_markup=main_keyboard)


@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Бот обладает следующими возможностями:"
                         "\n🟢 кнопка 'Статус' позволяет получить информацию о текущем состоянии стендов: отобразит статус-код, его описание и время, в которое был выполнен запрос;"
                         "\n🟢 кнопка 'Версия' отобразит информацию о версии UI, API и платформы, а также время запроса к серверу и стенд;", reply_markup=main_keyboard)

@router.message(F.text == 'Статус')
async def choose_stand_status(message: Message):
    await message.answer("Выберите стенд для проверки статуса:",
                         reply_markup=get_stand_choice_kb('status'),
                         parse_mode="Markdown")

@router.callback_query(F.data.startswith('status:'))
async def get_status_callback(callback: CallbackQuery):
    stand = callback.data.split(":")[1]  # 'lenta' или 'mars'
    await callback.answer(f"Запрашиваю статус для {stand}...")

    # Запрос к API с параметром
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/status/{stand}", timeout=10.0)

        if response.status_code == 200:
            data = response.json()
            msg = (f"💾 Стенд: {data['stand']}\n"
                   f"📊 Статус: {data['status']}\n"
                   f"📅 Дата: {data['date']} {data['timestamp']}\n"
                   f"📋 Описание: {data['description']}")
            await callback.message.answer(msg)
        else:
            await callback.message.answer(f"❌ Ошибка связи с API, код: {response.status_code}")
    except Exception as e:
        await callback.message.answer(f"⚠️ Не удалось связаться с API: {str(e)}")


@router.message(F.text == 'Версия')
async def choose_stand_version(message: Message):
    await message.answer(
        "🔢 Выберите стенд для проверки **версии**:",
        reply_markup=get_stand_choice_kb('version'),
        parse_mode="Markdown"
    )


@router.callback_query(F.data.startswith('version:'))
async def get_version_callback(callback: CallbackQuery):
    # Он достает название стенда из callback_data (например, 'mars')
    stand = callback.data.split(":")[1]

    await callback.answer(f"Получаю версию {stand}...")

    async with httpx.AsyncClient() as client:
        try:
            # Стучимся в API по новому адресу /{stand}
            response = await client.get(f"{API_URL}/version/{stand}", timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                text = f"🔢 **Стенд:** {data['stand']}\n**Версия:** `{data['version']}`"
            else:
                text = f"❌ Ошибка API: {response.status_code}"
        except Exception as e:
            text = f"⚠️ Ошибка: {str(e)}"

    # Отвечаем пользователю новым сообщением
    await callback.message.answer(text, parse_mode="Markdown")

@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery):
    await callback.message.delete()  # Удаляем сообщение с выбором стенда
    await callback.answer("Действие отменено")