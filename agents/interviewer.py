"""
Interviewer: ведёт диалог с кандидатом. Получает инструкцию от Observer и генерирует видимое сообщение.
"""
from llm_client import chat
from prompts import get_interviewer_system


def _history_to_messages(dialogue_history: list[dict]) -> list[dict]:
    """Конвертация истории в формат messages для API."""
    out = []
    for h in dialogue_history[-14:]:  # последние 14 реплик для контекста
        role = "user" if h.get("role") == "user" else "assistant"
        out.append({"role": role, "content": h.get("content", "")})
    return out


def run_interviewer(
    current_user_message: str,
    internal_thoughts: str,
    dialogue_history: list[dict],
    position: str,
    grade: str,
    experience: str,
    participant_name: str,
) -> str:
    """
    Interviewer генерирует ответ кандидату на основе инструкции Observer и контекста.
    Результат — agent_visible_message (то, что видит пользователь).
    """
    system = get_interviewer_system(position, grade, experience, participant_name)

    instruction = f"""Внутренняя инструкция от Observer (следуй ей, кандидат этого не видит):
---
{internal_thoughts}
---

Теперь сгенерируй ОДНО сообщение для кандидата: либо следующий вопрос, либо ответ на его вопрос, либо вежливое возвращение к интервью. Без префиксов и пометок."""

    messages = [{"role": "system", "content": system}]
    messages.extend(_history_to_messages(dialogue_history))
    messages.append({"role": "user", "content": current_user_message})
    messages.append({"role": "user", "content": instruction})

    return chat(messages)


def run_interviewer_first_message(
    position: str,
    grade: str,
    experience: str,
    participant_name: str,
) -> str:
    """
    Первый ход: приветствие и первый вопрос по позиции/грейду/опыту.
    Observer на первом ходе не вызывается (нечего оценивать).
    """
    system = get_interviewer_system(position, grade, experience, participant_name)
    user_prompt = """Сейчас начало интервью. Кандидат уже указал позицию, грейд и опыт (см. контекст выше).
Сгенерируй краткое приветствие и первый технический вопрос, уместный для этого грейда и опыта. Один блок текста без пометок."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_prompt},
    ]
    return chat(messages)
