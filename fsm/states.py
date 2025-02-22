from aiogram.fsm.state import State, StatesGroup

# для чата с ИИ
class ChatStates(StatesGroup):
    wait_for_request = State()