"""
Логгер сессии интервью.
Сохранение в interview_log.json в формате ТЗ:
participant_name, turns (turn_id, user_message, internal_thoughts, agent_visible_message), final_feedback.
"""
import json
import os
from typing import Any


def get_log_path(filename: str | None = None) -> str:
    base = filename or os.getenv("INTERVIEW_LOG_FILE", "interview_log.json")
    if not os.path.isabs(base):
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), base)
    return base


def init_log(participant_name: str, position: str, grade: str, experience: str) -> dict:
    """Инициализация структуры лога сессии."""
    return {
        "participant_name": participant_name,
        "position": position,
        "grade": grade,
        "experience": experience,
        "turns": [],
        "final_feedback": None,
    }


def append_turn(
    log: dict,
    turn_id: int,
    user_message: str,
    internal_thoughts: str,
    agent_visible_message: str,
) -> None:
    """Добавить один ход в лог. Порядок полей в turns: user_message, internal_thoughts, agent_visible_message."""
    log["turns"].append({
        "turn_id": turn_id,
        "user_message": user_message,
        "internal_thoughts": internal_thoughts,
        "agent_visible_message": agent_visible_message,
    })


def set_final_feedback(log: dict, feedback: str | dict) -> None:
    """Установить финальный фидбэк (строка или структурированный текст)."""
    if isinstance(feedback, dict):
        log["final_feedback"] = feedback
    else:
        log["final_feedback"] = feedback


def save_log(log: dict, filepath: str | None = None) -> str:
    """Сохранить лог в JSON. Возвращает путь к файлу."""
    path = get_log_path(filepath)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    return path
