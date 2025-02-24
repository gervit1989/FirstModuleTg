from aiogram import Router, F, types
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Descriptions import res_holder, command_description
from .CommandHandlers import command_start
from .base_commands import base_request, base_command
from fsm.states import CurrentChatWithCelebrityStates, QuizGame
from keyboards import keyboard_by_arg
from keyboards.callback_data import CelebrityData, QuizData

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'cb'))
async def select_celebrity(callback: CallbackQuery, callback_data: CelebrityData, state: FSMContext):
    await state.set_state(CurrentChatWithCelebrityStates.wait_for_answer)
    await state.update_data(name=callback_data.name, dialog=[])
    cb_res = res_holder.get_celebrity_resource(callback_data.name)
    photo_file = None
    if cb_res is not None:
        photo_file = cb_res.photo
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=f'Начните диалог со звездой по имени {callback_data.name}',
        reply_markup=keyboard_by_arg('TALK'),
    )

async def create_quiz_question(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data = await state.get_data()
    data['score'] = data.get('score', 0)
    data['dialog'] = data.get('dialog', [])
    await state.set_state(QuizGame.wait_for_answer)

    cb_res = res_holder.get_quiz_theme_resource(callback_data.name)
    photo_file = None
    name_of_theme = callback_data.name
    if cb_res is not None:
        photo_file = cb_res.photo
    else:
        name_of_theme = data['name']
        cb_res = res_holder.get_quiz_theme_resource(name_of_theme)
        if cb_res is not None:
            photo_file = cb_res.photo


    data['name'] = name_of_theme
    await state.update_data(data)

    request_message = [
        {
            'role': 'user',
            'content': name_of_theme,
        }
    ]
    await callback.bot.send_chat_action(
        chat_id=callback.from_user.id,
        action=ChatAction.TYPING,
    )
    ai_question = await base_request(callback, request_message, name_of_theme)
    if data['score'] == 0:
        ai_question = f'И мы начинаем наш квииииз с {callback.from_user.full_name}\nПервый вопрос:\n{ai_question}'
    data['question'] = ai_question
    await state.update_data(data)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=ai_question,
        reply_markup=keyboard_by_arg('QUIZ', True, True, 1),
    )

@callback_router.callback_query(QuizData.filter(F.button == 'qd'))
async def select_theme(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    await create_quiz_question(callback, callback_data, state)


@callback_router.callback_query(QuizData.filter(F.button == 'qd2'))
async def select_btn(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data = await state.get_data()
    if callback_data.name== 'SCORE_NULL':
        data['score'] = data.get('score', 0)
        if data['score'] > 0:
            data['score'] = 0
        data['dialog'] = []
        await state.update_data(data)
        text_msg = f'Счет обнулен для {callback.from_user.full_name}!'
        await callback.message.answer(
            text=text_msg,
            reply_markup = types.ReplyKeyboardRemove()
        )
    elif callback_data.name == 'NEXT_BY_THEME':
        await create_quiz_question(callback, callback_data, state)
    elif callback_data.name == 'CH_THEME':
        await base_command( callback.message, command_description['QUIZ'][0], 'QUIZ', None, False, True, True)
        await state.set_state(QuizGame.wait_for_request)
    elif callback_data.name == 'BACK':
        await state.clear()
        await command_start(callback.message)
    else:
        print(f'no btn{callback_data.name}')
