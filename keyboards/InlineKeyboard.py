import os
from Descriptions import *

from aiogram.utils.keyboard import InlineKeyboardBuilder

def ikb_celebrity():
    keyboard = InlineKeyboardBuilder()
    celebrities_list=[]

    # for item in resource_list:
    #     if isinstance(item, CelebrityResource):
    #         celebrities_list.append(item.celebrity_name)

    keyboard.adjust([1]*len(celebrities_list))
    return keyboard.as_markup(resize_keyboard=True,)

