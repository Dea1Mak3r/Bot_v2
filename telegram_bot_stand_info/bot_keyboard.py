from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Версия'), KeyboardButton(text='Статус')]
], resize_keyboard=True, input_field_placeholder='Выберите необходимое действие ниже')


def get_stand_choice_kb(action: str):
    """
    Генерирует инлайн-кнопки для выбора стенда.
    action: может быть 'status' или 'version'
    """
    # callback_data будет выглядеть как "status:lenta" или "version:mars"
    buttons = [
        [
            InlineKeyboardButton(text="🏢 Lenta", callback_data=f"{action}:lenta"),
            InlineKeyboardButton(text="🚀 Mars", callback_data=f"{action}:mars")
        ],
        # Можно добавить кнопку отмены, если пользователь передумал
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)