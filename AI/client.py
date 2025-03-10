
import httpx
from openai import AsyncOpenAI

from enum import Enum

from Descriptions import res_holder
from environment_holder import get_env_variable

class Model(Enum):
    TEXT_AI = ''


# класс ии клиента
class AI:
    _instance = None

    # синглтон
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance

    # конструктор
    def __init__(self):
        self._ai_token = get_env_variable('AI_TOKEN')
        self._proxy = get_env_variable('PROXY')
        self._model_of_ai = get_env_variable('AI_MODEL')
        self._client = self._create_client()

    # создание клиента
    def _create_client(self):
        print('creating client')
        # если прокси от JR
        if self._proxy == get_env_variable('PROXY'):
            ai_client = AsyncOpenAI(
                api_key=self._ai_token,
                http_client=httpx.AsyncClient(
                    proxy=self._proxy,
                )
            )
        else:
            ai_client = AsyncOpenAI(
                api_key=self._ai_token,
                base_url=self._proxy
            )
        return ai_client

    # установка модели ai
    def set_model_of_ai(self, ai_model=None):
        if ai_model is not None:
            self._model_of_ai = ai_model

    # переподключение
    def reconnect(self, token, proxy=None):
        if proxy is not None:
            self._proxy = proxy
        self._ai_token = token
        self._client = self._create_client()

    # получить промпт
    async def _read_prompt(self, path: str) -> str:
        print('path:', path)
        item = await res_holder.get_resource(path)
        if item is not None:
            prompt = item.prompt
        return prompt

    # текстовый запрос
    async def text_request(self, messages: list[dict[str, str]], prompt: str):
        message_list = list()
        message_list.append(
            {'role': 'system',
             'content': await self._read_prompt(prompt)},
        )
        for msg in messages:
            message_list.append(msg)
        completion = await self._client.chat.completions.create(
            messages=message_list,
            model=self._model_of_ai,
        )
        response = completion.choices[0].message.content
        return response
