"""
Прогон секретного сценария из ТЗ.
Вариант 1: с predefined_turns — реплики из списка, лог пишется автоматически.
Вариант 2: интерактивно — вводите реплики вручную по подсказкам.
Запуск: python run_scenario.py
"""
from main import run_interview

# Вводные по примеру сценария
PARTICIPANT_NAME = "Алекс"
POSITION = "Backend Developer"
GRADE = "Junior"
EXPERIENCE = "Пет-проекты на Django, немного SQL."

# Реплики кандидата по ходам (после приветствия агента)
CANDIDATE_TURNS = [
    # Ход 1 (Приветствие)
    "Привет. Я Алекс, претендую на позицию Junior Backend Developer. Знаю Python, SQL и Git.",
    # Ход 2 (Проверка знаний) — типичный развёрнутый ответ на вопрос про Python/бэкенд
    "Список в Python — изменяемая упорядоченная коллекция. Словарь — хеш-таблица ключ-значение. Кортеж — неизменяемый упорядоченный тип. Для бэкенда часто использую словари для JSON и списки для коллекций.",
    # Ход 3 (Ловушка / Hallucination Test)
    "Честно говоря, я читал на Хабре, что в Python 4.0 циклы for уберут и заменят на нейронные связи, поэтому я их не учу.",
    # Ход 4 (Смена ролей)
    "Слушайте, а какие задачи вообще будут на испытательном сроке? Вы используете микросервисы?",
    # Ход 5 (Завершение)
    "Стоп игра. Давай фидбэк.",
]


def run_scenario_automated():
    """Прогон сценария по списку реплик без ввода с клавиатуры."""
    print("=== Прогон секретного сценария (автоматический) ===\n")
    path = run_interview(
        participant_name=PARTICIPANT_NAME,
        position=POSITION,
        grade=GRADE,
        experience=EXPERIENCE,
        log_filepath="interview_log.json",
        predefined_turns=CANDIDATE_TURNS,
    )
    print(f"\nЛог сценария сохранён: {path}")
    return path


if __name__ == "__main__":
    run_scenario_automated()
