from Descriptions import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

# клавиатура звезд
def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    # достаем имена из хранилища
    celebrities_list=res_holder.get_celebrity_names()
    # выравниваем
    keyboard.adjust([1]*len(celebrities_list))
    # строим
    return keyboard.as_markup(resize_keyboard=True,)
