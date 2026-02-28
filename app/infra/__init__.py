"""Infrastructure integrations (HTTP clients, LLM clients)."""

from .funasr_client import transcribe as funasr_transcribe
from .llm_client import DEFAULT_BACKEND, raw_output, structured_output
from .marker_client import extract_file as marker_extract_file
from .paddle_client import extract_file as paddle_extract_file
from .url_config import (
	COSYVOICE_SYNTHESIZE_URL,
	FUNASR_TRANSCRIBE_PATH_URL,
	MARKER_EXTRACT_URL,
	OLLAMA_BASE_URL,
	OLLAMA_LLM_URL,
	OPENAI_LLM_URL,
	PADDLE_EXTRACT_PATH_URL,
	PADDLE_EXTRACT_URL,
)

__all__ = [
	"COSYVOICE_SYNTHESIZE_URL",
	"DEFAULT_BACKEND",
	"FUNASR_TRANSCRIBE_PATH_URL",
	"MARKER_EXTRACT_URL",
	"OLLAMA_BASE_URL",
	"OLLAMA_LLM_URL",
	"OPENAI_LLM_URL",
	"PADDLE_EXTRACT_PATH_URL",
	"PADDLE_EXTRACT_URL",
	"funasr_transcribe",
	"marker_extract_file",
	"paddle_extract_file",
	"raw_output",
	"structured_output",
]
