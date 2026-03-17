"""Static configuration for langchain_app."""

MODEL_NAME = "llama3.1:8b"
MODEL_PROVIDER = "ollama"
MODEL_BASE_URL = "http://localhost:8001"
MODEL_TEMPERATURE = 0.5
MODEL_MAX_TOKENS = 1000
SYSTEM_PROMPT = "You are an expert weather forecaster, who speaks in puns..."
DEFAULT_THREAD_ID = "1"
DEFAULT_USER_ID = "1"
DEFAULT_USER_MESSAGE = "what is the weather outside?"
