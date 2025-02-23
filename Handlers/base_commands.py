from aiogram.enums import ChatAction
from aiogram.types import Message
from openai import RateLimitError
from AI import ai_client
from Descriptions import res_holder
import os
from keyboards import keyboard_by_arg

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
    # проверка и заполнение request
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
            else:
                caption = req_msg
            # послать фото с подписью
            await message.answer_photo(
                photo=photo_file,
                caption=caption,
                reply_markup=keyboard_by_arg(arg_of_keyboard),
            )
        # если соединения нет, пробуем следующий токен
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
    print('done', arg_of_keyboard)