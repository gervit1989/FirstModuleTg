from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from Keyboard import keyboard_start

command_router = Router()


@command_router.message(F.text == 'Назад')
@command_router.message(Command('start'))
async def com_start(message: Message):
    await message.answer(
        text=f'Привет,{message.from_user.full_name}',
        reply_markup=keyboard_start(),
    )
    # for item in dict(message).items():
    #     print(item)


@command_router.message(Command('help'))
async def com_help(message: Message):
    await message.answer(
        text=f'Привет,{message.from_user.full_name}!'
    )
