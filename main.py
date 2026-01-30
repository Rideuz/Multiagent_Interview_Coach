"""
Multi-Agent Interview Coach — главный цикл.
Вводные: структурированные (имя, позиция, грейд, опыт, поведение) или неструктурированный текст (Extractor).
Диалог ведут Interviewer + Observer; вердикт — Manager; отчёт оформляет FeedbackWriter.
"""
import os
from interview_logger import init_log, append_turn, set_final_feedback, save_log
from agents.observer import run_observer
from agents.interviewer import run_interviewer, run_interviewer_first_message
from agents.extractor import extract_candidate_info
from feedback import generate_final_feedback
from candidate_input import normalize_candidate_input, candidate_input_to_run_params, load_candidate_from_json, CandidateInput


STOP_PHRASES = (
    "стоп интервью",
    "стоп игра",
    "давай фидбэк",
    "дай фидбэк",
    "завершить интервью",
    "конец интервью",
)


def is_stop_request(text: str) -> bool:
    t = (text or "").strip().lower()
    return any(phrase in t for phrase in STOP_PHRASES)


def run_interview(
    participant_name: str,
    position: str,
    grade: str,
    experience: str,
    log_filepath: str | None = None,
    predefined_turns: list[str] | None = None,
    behavior: list[str] | None = None,
) -> str:
    """
    Запуск интервью. Возвращает путь к сохранённому логу.
    predefined_turns — реплики кандидата по порядку (для сценария); если не задан, но задано behavior — используется behavior.
    """
    if predefined_turns is None and behavior:
        predefined_turns = behavior
    log = init_log(participant_name, position, grade, experience, behavior=behavior or (predefined_turns if predefined_turns else None))
    dialogue_history: list[dict] = []
    topics_covered: list[str] = []
    turn_id = 0

    # Первый ход: приветствие от агента (без ответа пользователя)
    turn_id += 1
    first_message = run_interviewer_first_message(position, grade, experience, participant_name)
    append_turn(
        log,
        turn_id=turn_id,
        user_message="",
        internal_thoughts="[Observer]: Старт интервью. [Interviewer]: Приглашение к представлению и первый контекст.",
        agent_visible_message=first_message,
    )
    dialogue_history.append({"role": "assistant", "content": first_message})

    print("\n--- Внутренние заметки (Observer) ---")
    print("[Observer]: Старт интервью. [Interviewer]: Приглашение к представлению и первый контекст.")
    print("\n--- Интервьюер ---")
    print(first_message)
    print()

    turn_index = 0
    while True:
        if predefined_turns is not None:
            if turn_index >= len(predefined_turns):
                break
            user_input = predefined_turns[turn_index].strip()
            turn_index += 1
            print("--- Вы (кандидат) ---")
            print(user_input)
            print()
        else:
            user_input = input("--- Вы (кандидат) ---\n").strip()
            if not user_input:
                continue

        if is_stop_request(user_input):
            turn_id += 1
            append_turn(
                log,
                turn_id=turn_id,
                user_message=user_input,
                internal_thoughts="[Observer]: Кандидат запросил завершение и фидбэк. [Interviewer]: Подготовка итогового отчёта.",
                agent_visible_message="Спасибо за беседу! Сейчас подготовлю итоговый отчёт.",
            )
            print("\n--- Интервьюер ---\nСпасибо за беседу! Сейчас подготовлю итоговый отчёт.\n")
            break

        turn_id += 1
        dialogue_history.append({"role": "user", "content": user_input})

        # Скрытая рефлексия: Observer анализирует ответ и даёт инструкцию
        internal_thoughts = run_observer(
            current_user_message=user_input,
            dialogue_history=dialogue_history,
            position=position,
            grade=grade,
            topics_covered=topics_covered,
        )
        print("\n--- Внутренние заметки (Observer) ---")
        print(internal_thoughts)

        # Interviewer генерирует видимое сообщение по инструкции Observer
        agent_message = run_interviewer(
            current_user_message=user_input,
            internal_thoughts=internal_thoughts,
            dialogue_history=dialogue_history,
            position=position,
            grade=grade,
            experience=experience,
            participant_name=participant_name,
        )

        append_turn(
            log,
            turn_id=turn_id,
            user_message=user_input,
            internal_thoughts=internal_thoughts,
            agent_visible_message=agent_message,
        )
        dialogue_history.append({"role": "assistant", "content": agent_message})

        print("\n--- Интервьюер ---")
        print(agent_message)
        print()

    # Генерация финального фидбэка
    print("Формирую итоговый отчёт...")
    feedback_text = generate_final_feedback(
        participant_name=participant_name,
        position=position,
        grade=grade,
        experience=experience,
        turns=log["turns"],
    )
    set_final_feedback(log, feedback_text)
    path = save_log(log, log_filepath)
    print("\n--- Финальный фидбэк ---")
    print(feedback_text)
    print(f"\nЛог сохранён: {path}")
    return path


def run_interview_from_candidate_input(
    candidate_input: CandidateInput | dict,
    log_filepath: str | None = None,
) -> str:
    """
    Запуск интервью из структурированного ввода (таблица 5 столбцов: имя, позиция, грейд, опыт, поведение).
    candidate_input: dict с ключами имя/name, позиция/position, грейд/grade, опыт/experience, поведение/behavior (список строк).
    """
    normalized = normalize_candidate_input(dict(candidate_input))
    params = candidate_input_to_run_params(normalized)
    return run_interview(
        participant_name=params["participant_name"],
        position=params["position"],
        grade=params["grade"],
        experience=params["experience"],
        log_filepath=log_filepath,
        predefined_turns=params.get("predefined_turns"),
        behavior=normalized.get("behavior"),
    )


def main():
    print("=== Multi-Agent Interview Coach ===\n")
    print("Режим ввода: 1 — пошагово (ФИО, позиция, грейд, опыт)")
    print("            2 — вставить текст самопрезентации (данные извлечёт агент Extractor)")
    print("            3 — путь к JSON с полями: имя, позиция, грейд, опыт, поведение (список ответов по вопросам)")
    mode = input("Выбор (1/2/3): ").strip() or "1"

    if mode == "2":
        text = input("Вставьте текст самопрезентации (например: Я Александр, 5 лет Backend...):\n").strip()
        if not text:
            print("Текст пуст, используем значения по умолчанию.")
            data = {}
        else:
            data = extract_candidate_info(text)
            print("Извлечено:", data)
        params = candidate_input_to_run_params(normalize_candidate_input(data))
        print("\nДля завершения введите: «Стоп интервью» или «Давай фидбэк».\n")
        run_interview(
            participant_name=params["participant_name"],
            position=params["position"],
            grade=params["grade"],
            experience=params["experience"],
            predefined_turns=params.get("predefined_turns"),
        )
        return

    if mode == "3":
        path = input("Путь к JSON-файлу: ").strip()
        if path and os.path.isfile(path):
            candidate = load_candidate_from_json(path)
            print("Загружено:", {k: v for k, v in candidate.items() if k != "behavior"}, "поведение: N пунктов" if candidate.get("behavior") else "")
            run_interview_from_candidate_input(candidate, log_filepath=None)
        else:
            print("Файл не найден. Запуск пошагового ввода.")
        return

    # Режим 1 — пошаговый ввод
    participant_name = input("ФИО кандидата (на русском): ").strip() or "Кандидат"
    position = input("Позиция (например, Backend Developer): ").strip() or "Backend Developer"
    grade = input("Грейд (Junior / Middle / Senior): ").strip() or "Junior"
    experience = input("Опыт (кратко): ").strip() or "Пет-проекты"
    print("\nДля завершения введите: «Стоп интервью» или «Давай фидбэк».\n")
    run_interview(participant_name, position, grade, experience)


if __name__ == "__main__":
    main()
