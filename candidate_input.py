"""
Структурированный ввод кандидата: {имя, позиция, грейд, опыт, поведение}.
Таблица/документ с 5 столбцами — преобразуется в этот формат.
Поведение: список пунктов «как отвечать на каждый вопрос» (для сценариев).
"""
import json
import re
from typing import TypedDict


class CandidateInput(TypedDict, total=False):
    """Структурированные данные кандидата (имя, позиция, грейд, опыт, поведение)."""
    name: str
    position: str
    grade: str
    experience: str
    behavior: list[str]


# Синонимы ключей для таблицы на русском
RUS_KEYS = {"имя": "name", "позиция": "position", "грейд": "grade", "опыт": "experience", "поведение": "behavior"}


def normalize_candidate_input(data: dict) -> CandidateInput:
    """
    Приводит ввод к единому формату: name, position, grade, experience, behavior.
    Принимает ключи на русском (имя, позиция, грейд, опыт, поведение) или на английском.
    behavior может быть списком строк или одной строкой (разбивается по переносам/точкам).
    """
    out: CandidateInput = {}
    for key, value in data.items():
        if value is None or value == "":
            continue
        norm_key = RUS_KEYS.get(key.strip().lower(), key.strip().lower())
        if norm_key == "behavior":
            if isinstance(value, list):
                out["behavior"] = [str(x).strip() for x in value if str(x).strip()]
            else:
                s = str(value).strip()
                # Разбить по пунктам: номера, переносы, точки с заглавной
                parts = []
                for part in s.replace(";", "\n").split("\n"):
                    part = part.strip()
                    if part:
                        # Убрать ведущий номер типа "1." "2)"
                        part = re.sub(r"^\s*\d+[.)]\s*", "", part).strip()
                        if part:
                            parts.append(part)
                out["behavior"] = parts if parts else [s] if s else []
        else:
            out[norm_key] = str(value).strip()
    return out


def candidate_input_to_run_params(c: CandidateInput) -> dict:
    """Преобразует CandidateInput в аргументы для run_interview."""
    return {
        "participant_name": c.get("name") or "Кандидат",
        "position": c.get("position") or "Developer",
        "grade": c.get("grade") or "Junior",
        "experience": c.get("experience") or "",
        "predefined_turns": c.get("behavior") if c.get("behavior") else None,
    }


def load_candidate_from_json(path: str) -> CandidateInput:
    """Загружает структурированный ввод из JSON-файла (одна запись или массив, берётся первая)."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list) and data:
        data = data[0]
    return normalize_candidate_input(data)
