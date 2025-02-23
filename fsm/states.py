from aiogram.fsm.state import State, StatesGroup

# для чата с ИИ
class ChatStates(StatesGroup):
    wait_for_request = State()

# для чата с ИИ-звездой
class ChatWithCelebrityStates(StatesGroup):
    wait_for_request = State()