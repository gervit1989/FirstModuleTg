from Descriptions import *
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callback_data import CelebrityData, QuizData


# клавиатура звезд
def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    # достаем имена из хранилища
    celebrities_list = res_holder.get_celebrity_names()
    lst_length = int(len(celebrities_list))
    print(celebrities_list, len(celebrities_list))

    for cb_name in celebrities_list:
        item = res_holder.get_celebrity_resource(cb_name)
        keyboard.button(text=cb_name,
                        callback_data=CelebrityData(
                            button='cb',
                            name=item.celebrity_name,
                        ), )

    # выравниваем
    keyboard.adjust(*[1] * lst_length)
    # строим
    return keyboard.as_markup()


# клавиатура квиза
def ikb_quiz():
    keyboard = InlineKeyboardBuilder()
    # достаем темы из хранилища
    themes = res_holder.get_quiz_names()
    lst_length = int(len(themes))
    print(themes, len(themes))

    for ru_theme_name in themes:
        item = res_holder.get_quiz_theme_resource_ru(ru_theme_name)
        print(item)
        keyboard.button(text=ru_theme_name,
                        callback_data=QuizData(
                            button='qd',
                            name=item.theme_name,
                        ), )

    # выравниваем
    keyboard.adjust(*[1] * lst_length)
    # строим
    return keyboard.as_markup()
