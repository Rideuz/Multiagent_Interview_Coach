"""
Генерация финального фидбэка через двух агентов:
Manager — только вердикт (grade, hiring_recommendation, confidence_score).
FeedbackWriter — только оформление итогового отчёта по структуре ТЗ.
"""
from agents.manager import run_manager_verdict
from agents.feedback_writer import run_feedback_writer


def generate_final_feedback(
    participant_name: str,
    position: str,
    grade: str,
    experience: str,
    turns: list[dict],
) -> str:
    """
    Генерирует структурированный финальный фидбэк: сначала Manager выносит вердикт,
    затем FeedbackWriter оформляет полный отчёт.
    """
    verdict = run_manager_verdict(
        participant_name=participant_name,
        position=position,
        grade=grade,
        experience=experience,
        turns=turns,
    )
    return run_feedback_writer(
        participant_name=participant_name,
        position=position,
        grade=grade,
        experience=experience,
        verdict=verdict,
        turns=turns,
    )
