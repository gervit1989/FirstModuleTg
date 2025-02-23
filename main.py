import asyncio  # асинхронка
import os       # файловая система

from aiogram import Bot, Dispatcher     # работа с тг
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.types import BotCommand, BotCommandScopeDefault  # команды меню

from Handlers import all_handlers_router
from Descriptions import *
from AI import *

# старт
def on_start():
    print("Bot is started...")

# завершение
def on_shutdown():
    print("Bot is turned down...")

# функция старта бота
async def start_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    dp.include_routers(
        all_handlers_router,
    )
    await set_commands(bot)
    await dp.start_polling(bot)

# установка команд
async def set_commands(bot: Bot):
    commands=[]
    print('setting commands')
    for item, value in command_description.items():
        commands.append(BotCommand(command=value[0], description=value[1]))
    photo_file = None
    item = await res_holder.get_resource('gpt')
    try:
        if item is not None:
            await bot.set_chat_photo(photo=item.photo, chat_id=os.getenv('CHATID'))
    except TelegramBadRequest:
        print('I can not change photo yet')
    await bot.set_my_commands(commands, BotCommandScopeDefault())

# запуск тг бота
if __name__ =='__main__':
    try:
        # запуск бота
        asyncio.run(start_bot())
    # пропускаем перезапуск бота - не ошибка
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        pass
    except TelegramNetworkError:
        print('TelegramNetworkError')
        pass