import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from AI import ai_client
from fsm.states import CurrentChatWithCelebrityStates
from keyboards import keyboard_by_arg
from Descriptions import text_descriptions, command_description, res_holder

from fsm import *
from aiogram.fsm.context import FSMContext

from .CommandHandlers import command_start
from .base_commands import base_command, base_request, base_answer

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


@ai_handler.message(CurrentChatWithCelebrityStates.wait_for_answer)
async def celebrity_answer(message: Message, state: FSMContext):
    user_text = 'Пока, всего тебе хорошего!' if message.text == text_descriptions['BACK_THIS'][0] or message.text == text_descriptions['BACK'][0] else message.text
    data = await state.get_data()
    user_request = {
        'role': 'user',
        'content': user_text,
    }
    data['dialog'].append(user_request)
    item = res_holder.get_celebrity_resource(data['name'])
    photo_file = None
    cmd_description = None
    if item is not None:
        photo_file =item.photo
        cmd_description = item.name_of_res

    celebrity_response = await base_request(message,data['dialog'], cmd_description)
    celebrity_response_dict = {
        'role': 'assistant',
        'content': celebrity_response,
    }
    data['dialog'].append(celebrity_response_dict)
    is_show = True
    if message.text == text_descriptions['BACK_THIS'][0]:
        is_show = False
    await state.update_data(dialog=data['dialog'])
    await message.answer_photo(
        photo=photo_file,
        caption=celebrity_response,
        reply_markup=keyboard_by_arg('TALK', False, is_show),
    )
    if message.text == text_descriptions['BACK'][0]:
        await state.clear()
        await command_start(message)
    if message.text == text_descriptions['BACK_THIS'][0]:
        await state.clear()
        await base_command(message, command_description['TALK'][0], 'TALK', None, False, True)
        await state.set_state(ChatWithCelebrityStates.wait_for_request)
