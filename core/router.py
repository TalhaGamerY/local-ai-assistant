from core.llm import OllamaLLM
from core.prompts import TOOL_DECISION_PROMPT


llm = OllamaLLM()


def decide_intent(user_text: str) -> str:
    lower = user_text.lower()

    # Fast rule-based routing first.
    if lower.startswith("open "):
        return "open_app"

    if "shutdown" in lower or "shut down" in lower:
        return "shutdown"

    if "restart" in lower:
        return "restart"

    if "news" in lower or "world right now" in lower or "current events" in lower:
        return "web_news"

    if lower.startswith("search file") or lower.startswith("find file"):
        return "search_files"

    if lower.startswith("list folder") or lower.startswith("show folder"):
        return "list_directory"

    if "fix this code" in lower or "error" in lower or "traceback" in lower:
        return "coding"

    if "what am i doing" in lower or "look at my screen" in lower:
        return "screen_context"

    # LLM fallback.
    decision = llm.generate(
        prompt=user_text,
        system=TOOL_DECISION_PROMPT,
    ).strip().lower()

    allowed = {
        "open_app",
        "search_files",
        "list_directory",
        "web_news",
        "shutdown",
        "restart",
        "coding",
        "screen_context",
        "normal_chat",
    }

    return decision if decision in allowed else "normal_chat"
