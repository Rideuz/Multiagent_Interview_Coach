"""
Клиент LLM (OpenAI-совместимый API: MuleRouter / OpenAI и др.).
"""
from openai import OpenAI
import config

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=config.API_KEY,
            base_url=config.BASE_URL,
        )
    return _client


def chat(messages: list[dict], model: str | None = None) -> str:
    """Один вызов chat completion. Возвращает content ответа."""
    client = get_client()
    model = model or config.MODEL
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    if not resp.choices:
        return ""
    return (resp.choices[0].message.content or "").strip()
