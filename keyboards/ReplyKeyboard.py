
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from Descriptions import *

def keyboard_start():
    keyboard = ReplyKeyboardBuilder()
    btn_count = 0
    for key, value in command_description.items():
        if len(value)>2:
            keyboard.button(text=value[2],)
            btn_count+=1
    keyboard.adjust([2]*btn_count/2)
    return keyboard.as_markup(resize_keyboard=True,)

def keyboard_btn_by_arg(arg: str):
    keyboard = ReplyKeyboardBuilder()
    for key, value in text_descriptions.items():
        if key is arg:
            keyboard.button(text=value[0],)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True,)

def keyboard_by_arg(arg: str):
    keyboard = ReplyKeyboardBuilder()
    for key, value in command_description.items():
        if key == arg:
            if len(value)>3:
                for i in range(3, len(value)):
                    for key2, value2 in text_descriptions.items():
                        if key2 is value[i]:
                            keyboard.button(text=value2[0],)
    keyboard.adjust(2,1)
    return keyboard.as_markup(resize_keyboard=True,)
