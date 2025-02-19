import os
import httpx
from aiohttp import request
from openai import AsyncOpenAI

from enum import Enum

from Descriptions import resource_list


class Model(Enum):
    TEXT_AI = ''

class AI:
    _instance = None

    # синглтон
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance=instance
        return cls._instance

    # конструктор
    def __init__(self):
        self._ai_token = os.getenv('AI_TOKEN')
        self._proxy = os.getenv('PROXY')
        self._client = self._create_client()

    # создание клиента
    def _create_client(self):
        ai_client = AsyncOpenAI(
            api_key=self._ai_token,
            http_client=httpx.AsyncClient(
                proxy=self._proxy,
            )
        )
        return ai_client

    # получить промпт
    async def _read_prompt(path: str) -> str:

        res_lst = await resource_list
        for item in res_lst:
            if item.name == path:
                prompt = await item.prompt
        return prompt

    # текстовый запрос
    async def text_request(self, messages: list[dict[str, str]], prompt: str):
        message_list = [
                           {'role': 'system',
                            'content': await self._read_prompt(prompt)},
                       ] + messages
        completion = await self._client.chat.completions.create(
            messages=message_list,
            model="gpt-3.5-turbo",
        )
        response = completion.choices[0].message.content
        return response


