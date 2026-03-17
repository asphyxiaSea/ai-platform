from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.memory import InMemorySaver

from langchain_app import config
from langchain_app.domain.schemas import Context, ResponseFormat
from langchain_app.domain.tools.weather_tools import (
    get_user_location,
    get_weather_for_location,
)
from langchain_app.infra.llm_factory import build_chat_model


def build_weather_agent():
    """Build and return the weather agent."""
    checkpointer = InMemorySaver()
    model = build_chat_model()
    return create_agent(
        model=model,
        system_prompt=config.SYSTEM_PROMPT,
        tools=[get_user_location, get_weather_for_location],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer,
    )
