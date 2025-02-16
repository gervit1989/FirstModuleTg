import asyncio  # асинхронка
import os       # файловая система
from importlib.metadata import files

from aiogram import Bot, Dispatcher     # работа с тг
from aiogram.types import BotCommand, BotCommandScopeDefault  # команды меню

from Handlers import *
from Definitions import *
from Descriptions import *

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

async def set_commands(bot: Bot):
    commands=[]
    for item, value in command_description.items():
        commands.append(BotCommand(command=value[0], description=value[1]))
    await bot.set_my_commands(commands, BotCommandScopeDefault())

if __name__ =='__main__':
    try:
        # собираем ресурсы
        init_resources()
        # запуск бота
        asyncio.run(start_bot())
    # пропускаем перезапуск бота - не ошибка
    except KeyboardInterrupt:
        pass