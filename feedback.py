"""
Генерация финального фидбэка по ТЗ:
Вердикт (Grade, Hiring Recommendation, Confidence), Hard Skills, Soft Skills, Roadmap.
"""
from llm_client import chat

FEEDBACK_SYSTEM = """Ты — агент, который формирует итоговый структурированный отчёт по результатам технического интервью.
Отчёт должен быть полезным артефактом для обучения кандидата.

Формат отчёта (строго придерживайся):

## Вердикт (Decision)
- **Grade**: Уровень кандидата (Junior / Middle / Senior) на основе ответов.
- **Hiring Recommendation**: Hire / No Hire / Strong Hire.
- **Confidence Score**: Уверенность в оценке в процентах (0-100%).

## Анализ Hard Skills (Technical Review)
- Таблица или список тем, затронутых в интервью.
- ** Confirmed Skills**: Темы, где кандидат дал точные ответы.
- ** Knowledge Gaps**: Темы, где были ошибки или кандидат сказал «не знаю». Для каждого такого пункта приведи правильный ответ (кратко).

## Анализ Soft Skills & Communication
- **Clarity**: Насколько понятно излагает мысли.
- **Honesty**: Пытался ли выкрутиться/соврать или честно признал незнание.
- **Engagement**: Задавал ли встречные вопросы.

## Персональный Roadmap (Next Steps)
- Список конкретных тем/технологий для подтягивания на основе выявленных пробелов.
- Опционально: ссылки на документацию или статьи (если знаешь актуальные).

Весь текст на русском. Не придумывай темы, которых не было в диалоге."""


def generate_final_feedback(
    participant_name: str,
    position: str,
    grade: str,
    experience: str,
    turns: list[dict],
) -> str:
    """
    Генерирует структурированный финальный фидбэк по всей сессии.
    turns: список {turn_id, user_message, internal_thoughts, agent_visible_message}.
    """
    dialogue_text = []
    for t in turns:
        dialogue_text.append(f"[Ход {t.get('turn_id', '?')}]")
        dialogue_text.append(f"Кандидат: {t.get('user_message', '')}")
        dialogue_text.append(f"Внутренние заметки: {t.get('internal_thoughts', '')}")
        dialogue_text.append(f"Интервьюер: {t.get('agent_visible_message', '')}")
        dialogue_text.append("")
    full_dialogue = "\n".join(dialogue_text)

    user_prompt = f"""Кандидат: {participant_name}
Позиция: {position}
Грейд: {grade}
Опыт: {experience}

Полный лог диалога (включая внутренние заметки Observer):
---
{full_dialogue}
---

Сформируй итоговый отчёт по формату выше."""

    messages = [
        {"role": "system", "content": FEEDBACK_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]
    return chat(messages)
