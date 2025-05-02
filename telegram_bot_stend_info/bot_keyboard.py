from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import CallbackQuery

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Версия'), KeyboardButton(text='Статус')]
], resize_keyboard=True, input_field_placeholder='Выберите необходимое действие ниже')