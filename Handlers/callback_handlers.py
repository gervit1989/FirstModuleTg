from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Descriptions import res_holder
from Handlers.base_commands import base_request
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

@callback_router.callback_query(QuizData.filter(F.button == 'qd'))
async def select_theme(callback: CallbackQuery, callback_data: QuizData, state: FSMContext):
    data = await state.get_data()
    data['score'] = data.get('score', 0)
    data['dialog'] = data.get('dialog',[])
    await state.set_state(QuizGame.wait_for_answer)
    data['name'] = callback_data.name
    await state.update_data(data)
    cb_res = res_holder.get_quiz_theme_resource(callback_data.name)
    photo_file = None
    if cb_res is not None:
        photo_file = cb_res.photo

    request_message = [
        {
            'role': 'user',
            'content': callback_data.name,
        }
    ]
    await callback.bot.send_chat_action(
        chat_id=callback.from_user.id,
        action=ChatAction.TYPING,
    )
    ai_question = await base_request(callback, request_message, callback_data.name)
    if data['score'] == 0:
        ai_question = f'И мы начинаем наш квииииз с {callback.from_user.full_name}\nПервый вопрос:\n{ai_question}'
    data['question'] = ai_question
    await state.update_data(data)
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo_file,
        caption=ai_question,
        reply_markup=keyboard_by_arg('QUIZ',True, True, 1),
    )

