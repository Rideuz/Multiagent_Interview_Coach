"""
Состояние сессии интервью для мультиагентного workflow.
Контекст: история диалога, темы, оценка ответов, флаг завершения.
"""
from typing import TypedDict


class InterviewState(TypedDict, total=False):
    """Состояние интервью между ходами."""

    participant_name: str
    position: str
    grade: str
    experience: str

    # История для контекста (последние N пар user/agent)
    dialogue_history: list[dict]  # [{"role": "user"|"assistant", "content": str}, ...]

    # Текущий ход
    current_user_message: str
    internal_thoughts: str  # вывод Observer (скрытая рефлексия)
    agent_visible_message: str  # ответ Interviewer пользователю

    # Уже затронутые темы (чтобы не спрашивать повторно)
    topics_covered: list[str]

    # Адаптивность: оценка последних ответов ("strong" | "ok" | "weak")
    recent_answer_quality: list[str]
    current_difficulty: str  # "easy" | "medium" | "hard"

    # Флаг: пользователь запросил фидбэк / стоп
    is_finished: bool

    # Собранные факты для фидбэка (темы, правильные/неправильные ответы)
    feedback_notes: list[dict]  # [{topic, correct: bool, user_answer, correct_answer?}, ...]
