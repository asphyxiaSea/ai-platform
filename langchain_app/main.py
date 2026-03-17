from pprint import pprint

from langchain_core.runnables import RunnableConfig

from langchain_app import config
from langchain_app.application.agent_factory import build_weather_agent
from langchain_app.application.result_extractor import extract_agent_result
from langchain_app.domain.schemas import Context


def run() -> dict:
    """Execute one weather-agent run and return extracted output."""
    agent = build_weather_agent()
    runnable_config: RunnableConfig = {
        "configurable": {"thread_id": config.DEFAULT_THREAD_ID}
    }

    response = agent.invoke(
        {"messages": [{"role": "user", "content": config.DEFAULT_USER_MESSAGE}]},
        config=runnable_config,
        context=Context(user_id=config.DEFAULT_USER_ID),
    )
    return extract_agent_result(response)


def main() -> None:
    pprint(run())


if __name__ == "__main__":
    main()
