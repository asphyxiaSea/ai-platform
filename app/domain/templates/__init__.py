"""Task templates for orchestration."""

from .files_parse import FilesTaskConfig, build_files_parse_task
from .llm_chat import LLMTaskConfig, LLMTaskMode, build_llm_task
from .voice_transcribe import (
	VoiceTaskConfig,
	VoiceTaskConfig_factory,
	VoiceTaskMode,
	build_voice_task,
)

__all__ = [
	"FilesTaskConfig",
	"LLMTaskConfig",
	"LLMTaskMode",
	"VoiceTaskConfig",
	"VoiceTaskConfig_factory",
	"VoiceTaskMode",
	"build_files_parse_task",
	"build_llm_task",
	"build_voice_task",
]
