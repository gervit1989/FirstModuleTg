from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from Descriptions import *
from keyboards.ReplyKeyboard import keyboard_start

command_router = Router()

@command_router.message(F.text == text_descriptions['BACK'][0])
@command_router.message(Command(command_description['START'][0]))
async def com_start(message: Message):
    await message.answer(
        text=f'Привет,{message.from_user.full_name}',
        reply_markup=keyboard_start(),
    )


@command_router.message(Command(command_description['HELP'][0]))
async def com_help(message: Message):
    await message.answer(
        text=f'Привет,{message.from_user.full_name}!'
    )
