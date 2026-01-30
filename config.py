"""
Конфигурация: API-ключ и настройки LLM.
MuleRouter — OpenAI-совместимый API (ключ sk-mr-...).
"""
import os
from dotenv import load_dotenv

load_dotenv()

# MuleRouter API (OpenAI-совместимый)
API_KEY = os.getenv("MULEROUTER_API_KEY", "sk-mr-55d5a63175c799eb1cbbf05f97fc0e76372b9a12ee0e5fbe731988f67ae587c5")
BASE_URL = os.getenv("MULEROUTER_BASE_URL", "https://api.mulerouter.ai/v1")  # при необходимости заменить
MODEL = os.getenv("INTERVIEW_LLM_MODEL", "qwen3-max")  # или qwen-plus, qwen-flash

# Лог сессии
LOG_FILE = os.getenv("INTERVIEW_LOG_FILE", "interview_log.json")
