"""
Конфигурация: API-ключ и настройки LLM.
MuleRouter — OpenAI-совместимый API.
"""
import os
from dotenv import load_dotenv
load_dotenv()
# LLM API: MuleRouter (документация: https://mulerouter.ai/docs/api-reference/endpoint/openai/chat)
API_KEY = os.getenv("MULEROUTER_API_KEY", "Your-api-Key")
BASE_URL = os.getenv("MULEROUTER_BASE_URL", "https://api.mulerouter.ai/vendors/openai/v1")
# Для OpenAI: задайте OPENAI_API_KEY и MULEROUTER_BASE_URL= (пусто) или USE_OPENAI=1
USE_OPENAI = os.getenv("USE_OPENAI", "").lower() in ("1", "true", "yes")
if USE_OPENAI:
    API_KEY = os.getenv("OPENAI_API_KEY", API_KEY)
    BASE_URL = None  # OpenAI client использует api.openai.com
MODEL = os.getenv("INTERVIEW_LLM_MODEL", "qwen3-max")

# Лог сессии
LOG_FILE = os.getenv("INTERVIEW_LOG_FILE", "interview_log.json")
