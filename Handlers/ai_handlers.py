import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from .CommandHandlers import command_start
from keyboards import keyboard_by_arg
from Descriptions import text_descriptions, command_description

from fsm import *
from aiogram.fsm.context import FSMContext

from .base_commands import base_command

ai_handler = Router()

@ai_handler.message(F.text == text_descriptions['FACT_NEW'][0])
@ai_handler.message(Command(command_description['FACT'][0]))
@ai_handler.message(F.text == command_description['FACT'][1])
async def ai_random_fact(message: Message):
    # вызов базовой структуры с командой random
    await base_command(message, command_description['FACT'][0], 'FACT')

@ai_handler.message(ChatStates.wait_for_request)
async def ai_chat(message: Message, state: FSMContext):
    #print(message.text)
    if message.text == text_descriptions['BACK'][0]:
        await state.clear()
        await command_start(message)
    else:
        request = message.text
        # вызов базовой структуры с командой gpt
        await base_command(message, command_description['AICHAT'][0], 'AICHAT', request)


@ai_handler.message(Command(command_description['QUIZ'][0]))
@ai_handler.message(F.text == command_description['QUIZ'][1])
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'В будущем здесь чат с ИИ -QUIZ',
        reply_markup=keyboard_by_arg('QUIZ')
    )
