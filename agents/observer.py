"""
Observer (Наблюдатель/Критик): анализирует ответ кандидата «в кулуарах» и даёт инструкцию Интервьюеру.
Скрытая рефлексия — пользователь не видит этот вывод; он пишется в internal_thoughts в лог.
"""
from typing import Any
from llm_client import chat
from prompts import OBSERVER_SYSTEM


def _history_to_text(history: list[dict]) -> str:
    parts = []
    for h in history[-10:]:  # последние 10 реплик
        role = "Кандидат" if h.get("role") == "user" else "Интервьюер"
        parts.append(f"{role}: {h.get('content', '')}")
    return "\n".join(parts) if parts else "(пока нет диалога)"


def run_observer(
    current_user_message: str,
    dialogue_history: list[dict],
    position: str,
    grade: str,
    topics_covered: list[str],
) -> str:
    """
    Observer анализирует последнее сообщение пользователя и возвращает внутреннюю инструкцию для Interviewer.
    Результат идёт в internal_thoughts в логе.
    """
    history_text = _history_to_text(dialogue_history)
    topics_text = ", ".join(topics_covered) if topics_covered else "пока нет"

    user_prompt = f"""Текущий ответ кандидата:
---
{current_user_message}
---

Предыдущий диалог (последние реплики):
---
{history_text}
---

Уже затронутые темы: {topics_text}

Дай инструкцию для Интервьюера: что сказать или спросить дальше, с учётом оценки ответа, офф-топика/галлюцинаций и контекста."""

    messages = [
        {"role": "system", "content": OBSERVER_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]
    return chat(messages)
