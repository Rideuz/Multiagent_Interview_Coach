"""
Агент Manager: единственная задача — принять вердикт по итогам интервью.
Не ведёт диалог, не проверяет факты, не форматирует отчёт. Только: Grade, Hiring Recommendation, Confidence.
"""
import json
import re
from llm_client import chat

MANAGER_SYSTEM = """Ты — агент Manager (принимающий решение о найме). Твоя единственная задача: на основе лога интервью вынести вердикт.

Ты НЕ ведёшь диалог и НЕ составляешь текст отчёта. Ты только возвращаешь решение в формате JSON.

Формат ответа — строго один JSON-объект с ключами:
- grade: уровень кандидата — ровно одно из: "Junior", "Middle", "Senior"
- hiring_recommendation: ровно одно из: "Hire", "No Hire", "Strong Hire"
- confidence_score: число от 0 до 100 (уверенность в оценке в процентах)

Никакого текста до или после JSON. Только валидный JSON."""


def run_manager_verdict(
    participant_name: str,
    position: str,
    grade: str,
    experience: str,
    turns: list[dict],
) -> dict:
    """
    Manager выносит вердикт по сессии. Возвращает dict: {grade, hiring_recommendation, confidence_score}.
    """
    dialogue = []
    for t in turns:
        dialogue.append(f"Кандидат: {t.get('user_message', '')}")
        dialogue.append(f"Заметки: {t.get('internal_thoughts', '')}")
        dialogue.append(f"Интервьюер: {t.get('agent_visible_message', '')}")
    text = "\n".join(dialogue)

    user_prompt = f"""Кандидат: {participant_name}
Позиция: {position}
Грейд заявленный: {grade}
Опыт: {experience}

Лог интервью:
---
{text}
---

Вердикт (JSON): grade, hiring_recommendation, confidence_score."""

    messages = [
        {"role": "system", "content": MANAGER_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]
    raw = chat(messages)
    # Извлечь первый полный JSON-объект (поддержка переносов строк)
    start = raw.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(raw)):
            if raw[i] == "{":
                depth += 1
            elif raw[i] == "}":
                depth -= 1
                if depth == 0:
                    raw = raw[start : i + 1]
                    break
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {}
    return {
        "grade": (data.get("grade") or "Junior").strip(),
        "hiring_recommendation": (data.get("hiring_recommendation") or "No Hire").strip(),
        "confidence_score": max(0, min(100, int(data.get("confidence_score", 50)))),
    }
