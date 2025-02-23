from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Descriptions import res_holder
from fsm.states import CurrentChatWithCelebrityStates
from keyboards import keyboard_by_arg
from keyboards.callback_data import CelebrityData

callback_router = Router()

@callback_router.callback_query(CelebrityData.filter(F.button=='cb'))
async def select_celebrity(callback: CallbackQuery, callback_data: CelebrityData, state: FSMContext):
    await state.set_state(CurrentChatWithCelebrityStates.wait_for_answer)
    await state.update_data(name=callback_data.name, dialog=[])
    cb_res = res_holder.get_celebrity_resource(callback_data.name)
    photo_file=None
    if cb_res is not None:
        photo_file=cb_res.photo
    await callback.bot.send_photo(
        chat_id = callback.from_user.id,
        photo=photo_file,
        caption=f'Начните диалог со звездой по имени {callback_data.name}',
        reply_markup=keyboard_by_arg('TALK'),
    )