from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from Descriptions import *
from Handlers.ai_handlers import base_command
from keyboards import *

command_router = Router()

@command_router.message(F.text == text_descriptions['BACK'][0])
@command_router.message(Command(command_description['START'][0]))
async def command_start(message: Message):
    await message.answer(
        text=f'Привет,{message.from_user.full_name}',
        reply_markup=keyboard_start(),
    )

@command_router.message(Command(command_description['AICHAT'][0]))
@command_router.message(F.text == command_description['AICHAT'][1])
async def command_gpt(message: Message):
    base_command(message, command_description['AICHAT'][0], 'AI_CHAT', None, False)

@command_router.message(Command(command_description['HELP'][0]))
async def command_help(message: Message):
    await message.answer(
        text=f'Привет,{message.from_user.full_name}!'
    )
