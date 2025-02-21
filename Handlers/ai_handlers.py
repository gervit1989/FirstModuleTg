import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from openai import RateLimitError

from keyboards import *
from Definitions import ai_client
from Descriptions import res_holder, text_descriptions, command_description
ai_handler = Router()

@ai_handler.message(F.text == text_descriptions['FACT_NEW'])
@ai_handler.message(Command(command_description['FACT'][0]))
@ai_handler.message(F.text == command_description['FACT'][1])
async def ai_random_fact(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    caption = None
    photo_file = None
    req_msg = ''
    item = await res_holder.get_resource(command_description['FACT'][0])
    if item is not None:
        #print(item.name_of_res, item.prompt)
        caption =  item.prompt
        photo_file = item.photo
        req_msg = item.msg
        #print('found', req_msg, photo_file, caption)
    request_message = [
        {
            'role': 'user',
            'content': req_msg,
        }
    ]
    try:
        caption = await ai_client.text_request(request_message, command_description['FACT'][0])
        await message.answer_photo(
            photo=photo_file,
            caption=caption,
            reply_markup=keyboard_btn_by_arg('FACT'),
        )
    except RateLimitError as e:
        print('try next token. this not done with: ',e)
        try:
            ai_client.reconnect(os.getenv('AI_TOKEN2'))
            print('1')
            caption = await ai_client.text_request(request_message, command_description['FACT'][0])
            print('2')
            await message.answer_photo(
                photo=photo_file,
                caption=caption,
                reply_markup=keyboard_btn_by_arg('FACT'),
            )
        except RateLimitError as e:
            print('we need new token and proxy by error:', e)
    finally:
        print('done')

@ai_handler.message(Command(command_description['AICHAT'][0]))
@ai_handler.message(F.text == command_description['AICHAT'][1])
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'В будущем здесь чат с ИИ',
        reply_markup=keyboard_by_arg('AI_CHAT')
    )

@ai_handler.message(Command(command_description['QUIZ'][0]))
@ai_handler.message(F.text == command_description['QUIZ'][1])
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'В будущем здесь чат с ИИ -QUIZ',
        reply_markup=keyboard_by_arg('QUIZ')
    )
