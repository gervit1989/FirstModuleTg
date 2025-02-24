from aiogram.fsm.state import State, StatesGroup


# для чата с ИИ
class ChatStates(StatesGroup):
    wait_for_request = State()


# для чата с ИИ-звездой
class ChatWithCelebrityStates(StatesGroup):
    wait_for_request = State()


# для чата с конкретной ИИ-звездой
class CurrentChatWithCelebrityStates(StatesGroup):
    wait_for_answer = State()


# для квиза
class QuizGame(StatesGroup):
    wait_for_answer = State()
    wait_for_request = State()
