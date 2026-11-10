import json
from datetime import datetime
from config import SHORT_TERM_MEMORY_FILE


def load_memory() -> dict:
    if not SHORT_TERM_MEMORY_FILE.exists():
        return {"messages": [], "screen": []}

    try:
        with open(SHORT_TERM_MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {"messages": [], "screen": []}


def save_memory(memory: dict) -> None:
    SHORT_TERM_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SHORT_TERM_MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=2)


def add_message(role: str, content: str) -> None:
    memory = load_memory()

    memory.setdefault("messages", []).append(
        {
            "role": role,
            "content": content,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )

    memory["messages"] = memory["messages"][-20:]
    save_memory(memory)


def add_screen_context(summary: str) -> None:
    memory = load_memory()

    memory.setdefault("screen", []).append(
        {
            "summary": summary,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )

    memory["screen"] = memory["screen"][-8:]
    save_memory(memory)


def get_recent_screen_context() -> str:
    memory = load_memory()
    screen_items = memory.get("screen", [])

    if not screen_items:
        return "No screen context available."

    return "\n".join(
        f"[{item['time']}] {item['summary']}" for item in screen_items[-5:]
    )
