from aiogram.utils.keyboard import ReplyKeyboardBuilder

def keyboard_start():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='ChatGPT',
    )
    keyboard.button(
        text='Помощь',
    )
    keyboard.button(
        text='Выход',
    )
    keyboard.adjust(2,1)
    return keyboard.as_markup(resize_keyboard=True,)

def keyboard_back():
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='Назад',
    )
    return keyboard.as_markup(resize_keyboard=True,)
