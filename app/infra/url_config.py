import os

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:8001")

_ollama_base = OLLAMA_BASE_URL.rstrip("/")

OLLAMA_LLM_URL = os.environ.get(
	"OLLAMA_LLM_URL",
	f"{_ollama_base}/api/chat",
)
OPENAI_LLM_URL = os.environ.get(
	"OPENAI_LLM_URL",
	f"{_ollama_base}/v1",
)

PADDLE_EXTRACT_URL = os.environ.get(
	"PADDLE_EXTRACT_URL",
	"http://localhost:8003/paddle/pp-structurev3/predict",
)
MARKER_EXTRACT_URL = os.environ.get(
	"MARKER_EXTRACT_URL",
	"http://localhost:8004/marker/extract",
)

FUNASR_TRANSCRIBE_PATH_URL = os.environ.get(
	"FUNASR_TRANSCRIBE_PATH_URL",
	"http://localhost:8005/funasr/transcribe_path",
)