from aiogram import Router
from .CommandHandlers import command_router
from .KeyBoardHandlers import keyboard_router
from .callback_handlers import callback_router

# объект роутер
all_handlers_router = Router()

# собираем все блоки в рамках package
all_handlers_router.include_routers(
    command_router, # команды
    keyboard_router,        # клавиатура
    callback_router,
)

__all__ = [
    'all_handlers_router',
]