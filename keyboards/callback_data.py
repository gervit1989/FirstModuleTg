from aiogram.filters.callback_data import CallbackData


# Данные для звезд
class CelebrityData(CallbackData, prefix='CD'):
    button: str
    name: str


# Данные для квиз
class QuizData(CallbackData, prefix='QD'):
    button: str
    name: str
