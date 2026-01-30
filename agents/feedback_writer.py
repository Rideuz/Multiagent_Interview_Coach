"""
Агент FeedbackWriter: единственная задача — оформить итоговый отчёт по структуре ТЗ.
Не принимает вердикт (это делает Manager). Получает вердикт и заметки по сессии и собирает текст.
"""
from llm_client import chat

FEEDBACK_WRITER_SYSTEM = """Ты — агент оформления отчёта. Твоя единственная задача: по вердикту Manager и логу интервью сформировать итоговый текст отчёта для кандидата.

Ты НЕ принимаешь решение о найме — вердикт тебе передаётся готовым. Ты только форматируешь отчёт.

Структура отчёта (строго придерживайся):

## Вердикт (Decision)
- **Grade**: <из вердикта>
- **Hiring Recommendation**: <из вердикта>
- **Confidence Score**: <из вердикта>%

## Анализ Hard Skills (Technical Review)
- Темы, затронутые в интервью.
- ** Confirmed Skills**: темы, где кандидат ответил верно.
- ** Knowledge Gaps**: темы с ошибками или «не знаю»; для каждого кратко приведи правильный ответ.

## Анализ Soft Skills & Communication
- **Clarity**: насколько понятно излагает мысли.
- **Honesty**: честность (признание незнания vs попытки выкрутиться).
- **Engagement**: встречные вопросы, вовлечённость.

## Персональный Roadmap (Next Steps)
- Конкретные темы/технологии для подтягивания по выявленным пробелам.
- Опционально: ссылки на документацию или статьи.

Весь текст на русском. Не придумывай тем, которых не было в диалоге."""


def run_feedback_writer(
    participant_name: str,
    position: str,
    grade: str,
    experience: str,
    verdict: dict,
    turns: list[dict],
) -> str:
    """
    FeedbackWriter формирует итоговый текст отчёта из вердикта Manager и лога.
    verdict: {grade, hiring_recommendation, confidence_score}.
    """
    dialogue = []
    for t in turns:
        dialogue.append(f"Кандидат: {t.get('user_message', '')}")
        dialogue.append(f"Внутренние заметки: {t.get('internal_thoughts', '')}")
        dialogue.append(f"Интервьюер: {t.get('agent_visible_message', '')}")
    dialogue_text = "\n".join(dialogue)

    user_prompt = f"""Вердикт Manager (использовать как есть):
- Grade: {verdict.get('grade', 'Junior')}
- Hiring Recommendation: {verdict.get('hiring_recommendation', 'No Hire')}
- Confidence Score: {verdict.get('confidence_score', 0)}%

Кандидат: {participant_name}
Позиция: {position}
Опыт: {experience}

Лог интервью:
---
{dialogue_text}
---

Сформируй итоговый отчёт по структуре выше."""

    messages = [
        {"role": "system", "content": FEEDBACK_WRITER_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]
    return chat(messages)
