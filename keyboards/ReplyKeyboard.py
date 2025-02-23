
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from Descriptions import *
from .InlineKeyboard import ikb_celebrity

def keyboard_start():
    keyboard = ReplyKeyboardBuilder()
    btn_count = 0
    for key, value in command_description.items():
        if len(value)>2:
            btn_txt = value[2]
            if value[2] == '-':
                btn_txt = value[1]
            keyboard.button(text=btn_txt,)
            btn_count+=1
    btn_count = btn_count//2
    #print('btns count:',btn_count)
    keyboard.adjust(*[2]*btn_count)
    return keyboard.as_markup(resize_keyboard=True,)

def keyboard_btn_by_arg(arg: str):
    keyboard = ReplyKeyboardBuilder()
    for key, value in text_descriptions.items():
        if key is arg:
            keyboard.button(text=value[0],)
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True,)

def keyboard_by_arg(arg: str):
    if arg == 'TALK':
        return ikb_celebrity()
    keyboard = ReplyKeyboardBuilder()
    #print('arg:', arg)
    btn_count = 0
    for key, value in command_description.items():
        #print('key:', key)
        if key == arg:
            #print('arg:', arg, len(value))
            if len(value)>3:
                for i in range(3, len(value)):
                    for key2, value2 in text_descriptions.items():
                        if key2 is value[i]:
                            keyboard.button(text=value2[0],)
                            btn_count += 1
    btn_count = btn_count//2
    keyboard.adjust(*[2]*btn_count)
    return keyboard.as_markup(resize_keyboard=True,)
