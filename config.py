from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OLLAMA_URL = "http://localhost:11434/api/generate"

TEXT_MODEL = "llama3.1:8b"
VISION_MODEL = "moondream"

ASSISTANT_NAME = "Jarvis"
USER_TITLE = "Sir"

SCREEN_EYE_INTERVAL_SECONDS = 5
SCREEN_EYE_ENABLED_BY_DEFAULT = False
SCREEN_MEMORY_LIMIT = 8

LOG_FILE = BASE_DIR / "logs" / "assistant.log"
SHORT_TERM_MEMORY_FILE = BASE_DIR / "memory" / "short_term.json"

# Safety settings
ALLOW_SHUTDOWN = True
ALLOW_RESTART = True

# Apps you allow the assistant to open directly.
APP_ALIASES = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "start chrome",
    "edge": "start msedge",
    "discord": "start discord",
    "steam": "start steam",
    "blender": "start blender",
    "vscode": "code",
}

# Folders the assistant can search without asking again.
SAFE_SEARCH_ROOTS = [
    str(Path.home() / "Desktop"),
    str(Path.home() / "Downloads"),
    str(Path.home() / "Documents"),
]
