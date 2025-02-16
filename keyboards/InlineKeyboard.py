import os
from collections import namedtuple

from aiogram.utils.keyboard import InlineKeyboardBuilder


def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    Celebrity = namedtuple('Celebrity', ['name', 'file_name'])
    files_list=[file for file in os.listdir('prompts') if file.startswith('talk_')]
    celebrities_list=[]
    for file in files_list:
        with open(os.path.join('prompts',file)) as txt_file:
            name = txt_file.read()

    keyboard.adjust([1]*len(celebrities_list))
    return keyboard.as_markup(resize_keyboard=True,)

