def extract_agent_result(state: dict):
    """Extract structured response with graceful fallbacks."""
    if "structured_response" in state:
        return state["structured_response"]

    if "output" in state:
        return state["output"]

    messages = state.get("messages") or []
    if not messages:
        return state

    last_message = messages[-1]

    tool_calls = getattr(last_message, "tool_calls", None) or []
    for call in reversed(tool_calls):
        args = call.get("args") if isinstance(call, dict) else None
        if args:
            return args

    additional = getattr(last_message, "additional_kwargs", None) or {}
    for key in ("structured_response", "parsed", "json"):
        if key in additional:
            return additional[key]

    return getattr(last_message, "content", state)
