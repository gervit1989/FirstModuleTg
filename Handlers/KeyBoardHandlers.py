from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from Descriptions import *
from keyboards.ReplyKeyboard import keyboard_by_arg, keyboard_btn_by_arg, keyboard_start

keyboard_router = Router()

@keyboard_router.message(Command(command_description['AICHAT'][0]))
@keyboard_router.message(F.text == command_description['AICHAT'][1])
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'В будущем здесь чат с ИИ',
        reply_markup=keyboard_by_arg('AI_CHAT')
    )

@keyboard_router.message(F.text == 'Выход')
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'Вы покидаете нас, как жаль!',
        reply_markup=keyboard_start()
    )

@keyboard_router.message(Command(command_description['HELP'][0]))
@keyboard_router.message(F.text == command_description['HELP'][1])
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'Вы смиренно просите нас о помощи, да предоставим вам требуемое!',
        reply_markup=keyboard_start()
    )