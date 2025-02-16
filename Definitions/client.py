import os
import httpx
from aiohttp import request
from openai import AsyncOpenAI

from enum import Enum

class Model(Enum):
    TEXT_AI = ''

class AI:
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super.__new__(cls)
            cls._instance=instance
        return cls._instance

    def __init__(self):
        self.ai_token = os.getenv('AI_TOKEN')
        self.proxy =os.getenv('PROXY')
        self._client = self.create_client()

    def _create_client(self):
        ai_client = AsyncOpenAI(
            api_key=self.ai_token,
            http_client=httpx.Client(
                proxy=self.proxy,
            )
        )
        return ai_client

    async def text_request(self, messages):
        response=''
        return response


