from langchain.chat_models import init_chat_model

from langchain_app import config


def build_chat_model():
    """Create the chat model used by the application."""
    return init_chat_model(
        config.MODEL_NAME,
        model_provider=config.MODEL_PROVIDER,
        base_url=config.MODEL_BASE_URL,
        temperature=config.MODEL_TEMPERATURE,
        max_tokens=config.MODEL_MAX_TOKENS,
    )
