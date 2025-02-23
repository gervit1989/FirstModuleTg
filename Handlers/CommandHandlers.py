from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from Descriptions import *
from keyboards import *
from aiogram.fsm.context import FSMContext
from fsm import *
from .base_commands import base_command, base_answer

command_router = Router()

@command_router.message(F.text == text_descriptions['BACK'][0])
@command_router.message(Command(command_description['START'][0]))
async def command_start(message: Message):
    await base_answer(message, 'main')

# - /gpt
@command_router.message(Command(command_description['AICHAT'][0]))
@command_router.message(F.text == command_description['AICHAT'][1])
async def command_gpt(message: Message, state: FSMContext):
    # поздороваться
    await base_command(message, command_description['AICHAT'][0], 'AICHAT', None, False)

    # сохраняем положение
    await state.set_state(ChatStates.wait_for_request)

# - /talk
@command_router.message(Command(command_description['TALK'][0]))
@command_router.message(F.text == command_description['TALK'][1])
async def command_gpt(message: Message, state: FSMContext):
    # поздороваться
    await base_command(message, command_description['TALK'][0], 'TALK', None, False, True)

    # сохраняем положение
    await state.set_state(ChatWithCelebrityStates.wait_for_request)

@command_router.message(Command(command_description['HELP'][0]))
async def command_help(message: Message):
    await message.answer(
        text=f'Помощь,{message.from_user.full_name}!'
    )
