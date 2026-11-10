from pathlib import Path
from config import SAFE_SEARCH_ROOTS


def list_directory(path: str) -> str:
    target = Path(path).expanduser()

    if not target.exists():
        return "That path does not exist."

    if not target.is_dir():
        return "That path is not a folder."

    items = []
    for item in target.iterdir():
        item_type = "Folder" if item.is_dir() else "File"
        items.append(f"{item_type}: {item.name}")

    return "\n".join(items[:200]) or "Folder is empty."


def search_files(filename_query: str) -> str:
    matches = []
    query = filename_query.lower().strip()

    for root in SAFE_SEARCH_ROOTS:
        root_path = Path(root)

        if not root_path.exists():
            continue

        for path in root_path.rglob("*"):
            try:
                if query in path.name.lower():
                    matches.append(str(path))
            except PermissionError:
                continue

            if len(matches) >= 50:
                break

    if not matches:
        return "No matching files found in safe search folders."

    return "\n".join(matches)
