from aiogram import Router, F
from aiogram.types import Message

from Keyboard import keyboard_back, keyboard_start

keyboard_router = Router()

@keyboard_router.message(F.text == 'ChatGPT')
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'В будущем здесь GPT',
        reply_markup=keyboard_back()
    )

@keyboard_router.message(F.text == 'Выход')
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'Вы покидаете нас, как жаль!',
        reply_markup=keyboard_start()
    )

@keyboard_router.message(F.text == 'Помощь')
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'Вы смиренно просите нас о помощи, да предоставим вам требуемое!',
        reply_markup=keyboard_start()
    )