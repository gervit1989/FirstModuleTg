from aiogram import Router
from .CommandHandlers import command_router
from .KeyBoardHandlers import keyboard_router

all_h_router = Router()
all_h_router.include_routers(
    command_router,
    keyboard_router,
)

__all__ =[
    'all_h_router',
]