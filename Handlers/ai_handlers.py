import os

from aiogram import Router, F, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command

from AI import ai_client
from fsm.states import CurrentChatWithCelebrityStates, QuizGame
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
    # print(message.text)
    if message.text == text_descriptions['BACK'][0]:
        await state.clear()
        await command_start(message)
    else:
        request = message.text
        # вызов базовой структуры с командой gpt
        await base_command(message, command_description['AICHAT'][0], 'AICHAT', request)


@ai_handler.message(CurrentChatWithCelebrityStates.wait_for_answer)
async def celebrity_answer(message: Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    user_text = 'Пока, всего тебе хорошего!' if message.text == text_descriptions['BACK_CB_LST'][0] or message.text == \
                                                text_descriptions['BACK'][0] else message.text
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
        photo_file = item.photo
        cmd_description = item.name_of_res

    celebrity_response = await base_request(message, data['dialog'], cmd_description)
    celebrity_response_dict = {
        'role': 'assistant',
        'content': celebrity_response,
    }
    data['dialog'].append(celebrity_response_dict)
    is_show = True
    if message.text == text_descriptions['BACK_CB_LST'][0]:
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
    if message.text == text_descriptions['BACK_CB_LST'][0]:
        await base_command(message, command_description['TALK'][0], 'TALK', None, False, True)
        await state.set_state(ChatWithCelebrityStates.wait_for_request)


@ai_handler.message(QuizGame.wait_for_answer)
async def quiz_answer(message: Message, state: FSMContext):
    is_inline_keyboard = True
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    data = await state.get_data()
    user_answer = message.text
    item = await res_holder.get_resource(data['name'])

    photo_file = item.photo if item is not None else None
    if user_answer == text_descriptions['NEXT_BY_THEME'][0] and not is_inline_keyboard:
        request_message = [
            {
                'role': 'user',
                'content': data['name'],
            }
        ]
        await message.bot.send_chat_action(
            chat_id=message.from_user.id,
            action=ChatAction.TYPING,
        )
        ai_question = await base_request(message, request_message, data['name'])
        if data['score'] == 0:
            ai_question = f'И мы начинаем наш квииииз с {message.from_user.full_name}\nПервый вопрос:\n{ai_question}'
        else:
            ai_question = f'Ваш счет {data['score']}\n{ai_question}'
        data['question'] = ai_question
        await state.update_data(data)
        await message.bot.send_photo(
            chat_id=message.from_user.id,
            photo=photo_file,
            caption=ai_question,
            reply_markup=keyboard_by_arg('QUIZ', True, True, 1),
        )
        return
    if user_answer== text_descriptions['SCORE_NULL'][0] and not is_inline_keyboard:
        data['score'] = data.get('score', 0)
        if data['score'] > 0:
            data['score'] = 0
        data['dialog'] = []
        await state.update_data(data)
        text_msg = f'Счет обнулен для {message.from_user.full_name}!'
        await message.answer(
            text=text_msg,
            reply_markup = types.ReplyKeyboardRemove()
        )
        return

    user_text = 'Пока, всего тебе хорошего!' if user_answer == text_descriptions['BACK'][0] else message.text
    quiz_question = data['question']
    user_request = list()
    user_request.append(
        {'role': 'assistant',
         'content': quiz_question})
    user_request.append(
        {'role': 'user',
         'content': user_answer})
    data['dialog'].append(user_request)
    cmd_description = None
    if item is not None:
        cmd_description = item.theme_name
    quiz_response = await base_request(message, user_request, cmd_description)
    correct_answer = quiz_response.split(' ', 1)[0]
    if correct_answer == 'Правильно!':
        data['score'] += 1
        await state.update_data(score=data['score'])
    quiz_response_dict = {
        'role': 'assistant',
        'content': quiz_response,
    }
    data['dialog'].append(quiz_response_dict)
    is_show = True
    stage_id = 1
    if message.text == text_descriptions['CH_THEME'][0] and not is_inline_keyboard:
        stage_id = 0
    await state.update_data(dialog=data['dialog'])
    await message.answer_photo(
        photo=photo_file,
        caption=quiz_response + f'\nВаш текущий счет: {data['score']}',
        reply_markup=keyboard_by_arg('QUIZ', is_inline_keyboard, is_show, stage_id),
    )
    if user_answer == text_descriptions['BACK'][0] and not is_inline_keyboard:
        await state.clear()
        await command_start(message)
    if user_answer == text_descriptions['CH_THEME'][0] and not is_inline_keyboard:
        await base_command(message, command_description['QUIZ'][0], 'QUIZ', None, False, True)
        await state.set_state(ChatWithCelebrityStates.wait_for_request)
