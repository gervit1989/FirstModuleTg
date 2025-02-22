import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ChatAction
from openai import RateLimitError

from Handlers.CommandHandlers import command_start
from keyboards import *
from Definitions import ai_client
from Descriptions import res_holder, text_descriptions, command_description

ai_handler = Router()

# базовая команда ИИ
async def base_command(message: Message, cmd_description: str, arg_of_keyboard: str, request:str = None, get_from_ai:bool = True):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    caption = None
    photo_file = None
    req_msg = ''
    item = await res_holder.get_resource(cmd_description)
    if item is not None:
        #print(item.name_of_res, item.prompt)
        caption =  item.prompt
        photo_file = item.photo
        req_msg = item.msg
        #print('found', req_msg, photo_file, caption)
    else:
        print(f'Хьюстон, у нас проблемы!{arg_of_keyboard}')
    if request is not None:
        req_msg = request
    #запрос
    request_message = [
        {
            'role': 'user',
            'content': req_msg,
        }
    ]
    # список подключений
    ai_client_connect_data = list()
    ai_client_connect_data.append((os.getenv('AI_TOKEN2'),))
    ai_client_connect_data.append((os.getenv('AI_TOKEN3'),os.getenv('PROXY2'),))
    ai_client_connect_data.append((os.getenv('AI_TOKEN'),os.getenv('PROXY'),))

    # попытка выполнить команду
    for i in range(len(ai_client_connect_data)):
        try:
            # подпись к картинке
            if get_from_ai:
                caption = await ai_client.text_request(request_message, cmd_description)
            # послать фото с подписью
            await message.answer_photo(
                photo=photo_file,
                caption=caption,
                reply_markup=keyboard_by_arg(arg_of_keyboard),
            )
        # если соедиенения нет, пробуем следующий токен
        except RateLimitError as e:
            print('try next token. this not done with: ',e)
            item = ai_client_connect_data[i]
            if len(item) < 2:
                ai_client.reconnect(item[0])
            else:
                ai_client.reconnect(item[0], item[1])
            await message.bot.send_chat_action(
                chat_id=message.from_user.id,
                action=ChatAction.TYPING,
            )
        else:
            break
    print('done')

@ai_handler.message(F.text == text_descriptions['FACT_NEW'][0])
@ai_handler.message(Command(command_description['FACT'][0]))
@ai_handler.message(F.text == command_description['FACT'][1])
async def ai_random_fact(message: Message):
    # вызов базовой структуры с командой random
    await base_command(message, command_description['FACT'][0], 'FACT')


async def ai_chat(message: Message, state: FSMContext):
    if message.text == text_descriptions['BACK']:
        await command_start(message)
    else:
        request = message.text
        # вызов базовой структуры с командой gpt
        await base_command(message, command_description['AICHAT'][0], 'AICHAT', request)


@ai_handler.message(Command(command_description['QUIZ'][0]))
@ai_handler.message(F.text == command_description['QUIZ'][1])
async def keyboard_chat(message: Message):
    await message.answer(
        text=f'В будущем здесь чат с ИИ -QUIZ',
        reply_markup=keyboard_by_arg('QUIZ')
    )
