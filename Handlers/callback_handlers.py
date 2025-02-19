from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
import os
from keyboards import ikb_celebrity

callback_router = Router()

@callback_router.callback_query(F.data.startswith('talk_'))
async def select_celebrity(callback: CallbackQuery):
    photo_file =FSInputFile(path=os.path.join('images', callback.data.file_name)),
    await callback.bot.send_photo(
        chat_id = callback.data,
        text = callback.data,
        photo=photo_file,
        show_alert=True,
        caption='Начните диалог со звездой',
        reply_markup=ikb_celebrity,
    )