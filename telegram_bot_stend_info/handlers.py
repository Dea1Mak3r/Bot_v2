from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio
from aiogram import Router
from aiogram import F
from bot_keyboard import main_keyboard
import requests
import json

router = Router()


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
async def get_status_command(message: Message):
    response = requests.get('http://127.0.0.1:8000/status')
    if response.status_code == 200:
        data = response.json()
        # status_messages = []
        """Если возвращаются 5 айтемов - один стенд"""
        if len(data) == 5:
            stand_message = (
                            f"Стенд: \t\t\t{data['stand']}\n\n"
                            f"Статус-код: \t\t\t{data['status']}\n\n"
                            f"Дата: \t\t\t{data['date']}\n\n"
                            f"Время: \t\t\t{data['timestamp']}\n\n"
                            f"Описание: \t\t\t{data['description']}\n\n"
                        )
        """Если получаем ответ от нескольких стендов"""
        # for stand in data:
    #         stand_message = (
    #             f"Стенд: \t\t\t{stand['stand']}\n\n"
    #             f"Статус-код: \t\t\t{stand['status']}\n\n"
    #             f"Дата: \t\t\t{stand['date']}\n\n"
    #             f"Время: \t\t\t{stand['timestamp']}\n\n"
    #             f"Описание: \t\t\t{stand['description']}\n\n"
    #         )
    #         status_messages.append(stand_message)
    #
    #     await message.answer("\n\n\n".join(status_messages))
    # else:
    #     await message.answer(f"Ошибка при получении статуса. Код ответа: {response.status_code}")
        await message.answer(stand_message)
    else:
        await message.answer(f"Ошибка при получении статуса. Код ответа: {response.status_code}")


@router.message(F.text == 'Версия')
async def get_version_command(message: Message):
    response = requests.get('http://127.0.0.1:8000/version')
    if response.status_code == 200:
        await message.answer(f"Версия стенда: {response.text}")
    else:
        await message.add_answer(f"Ошибка при получении статуса. Код ответа: {response.status_code}")
    #     data = response.json()
    #     version_messages = []
    #     for stand, info in data.items():
    #         version_message = (
    #             f"Стенд: \t\t\t{stand}\n\n"
    #             f"Дата последнего обновления: \t\t\t{info[0]}\n\n"
    #             f"Время: \t\t\t{info[1]}\n"
    #         )
    #         version_messages.append(version_message)
    #     await message.answer('\n\n\n'.join(version_messages))
    # else:
    #     await message.add_answer(f"Ошибка при получении статуса. Код ответа: {response.status_code}")