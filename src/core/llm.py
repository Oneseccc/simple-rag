from __future__ import annotations

from abc import ABC, abstractmethod

import httpx
from groq import Groq

from src.config import settings


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str: ...

    @abstractmethod
    def get_model_name(self) -> str: ...

    @abstractmethod
    def get_provider_name(self) -> str: ...


class GroqProvider(LLMProvider):
    def __init__(self):
        self._client = Groq(api_key=settings.GROQ_API_KEY)
        self._model = settings.GROQ_MODEL

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=0.1,
            max_tokens=2048,
        )
        return response.choices[0].message.content

    def get_model_name(self) -> str:
        return self._model

    def get_provider_name(self) -> str:
        return "groq"


class OllamaProvider(LLMProvider):
    def __init__(self):
        self._base_url = settings.OLLAMA_BASE_URL
        self._model = settings.OLLAMA_MODEL

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.1},
                },
            )
            response.raise_for_status()
            return response.json()["message"]["content"]

    def get_model_name(self) -> str:
        return self._model

    def get_provider_name(self) -> str:
        return "ollama"


def get_llm_provider() -> LLMProvider:
    if settings.LLM_PROVIDER == "ollama":
        return OllamaProvider()
    return GroqProvider()
