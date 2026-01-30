"""
Агент Extractor: единственная задача — извлечь из неструктурированного текста
поля {имя, позиция, грейд, опыт}. Не анализирует ответы и не ведёт диалог.
"""
import json
import re
from llm_client import chat

EXTRACTOR_SYSTEM = """Ты — агент извлечения данных. Твоя единственная задача: по тексту кандидата (приветствие, самопрезентация) извлечь структурированные поля.

Вход: произвольный текст, например: "Я Александр, 5 лет работаю Python Backend-разработчиком, сейчас на Senior позиции, имею опыт в Django, PostgreSQL..."

Выход: строго один JSON-объект с ключами (все строки, на русском где уместно):
- name: ФИО или имя кандидата
- position: должность/позиция (например Backend Developer, Frontend developer)
- grade: грейд — только одно из: Junior, Middle, Senior (если неясно — Junior)
- experience: краткое описание опыта (1-2 предложения)

Не добавляй других ключей. Не комментируй. Только валидный JSON."""


def extract_candidate_info(unstructured_text: str) -> dict:
    """
    Извлекает имя, позицию, грейд, опыт из неструктурированного сообщения.
    Возвращает dict: {name, position, grade, experience}.
    """
    messages = [
        {"role": "system", "content": EXTRACTOR_SYSTEM},
        {"role": "user", "content": unstructured_text.strip() or "Кандидат не написал ничего."},
    ]
    raw = chat(messages)
    # Попытка вытащить JSON из ответа (на случай если модель обернула в markdown)
    json_match = re.search(r"\{[^{}]*\}", raw, re.DOTALL)
    if json_match:
        raw = json_match.group(0)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {}
    return {
        "name": (data.get("name") or "Кандидат").strip(),
        "position": (data.get("position") or "Developer").strip(),
        "grade": (data.get("grade") or "Junior").strip(),
        "experience": (data.get("experience") or "").strip(),
    }
