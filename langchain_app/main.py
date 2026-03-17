from __future__ import annotations

import os

import uvicorn

from langchain_app.fastapi_app import app


def main() -> None:
    host = os.environ.get("LANGCHAIN_APP_HOST", "0.0.0.0")
    port = int(os.environ.get("LANGCHAIN_APP_PORT", "8010"))
    reload = os.environ.get("LANGCHAIN_APP_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "langchain_app.main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    main()
