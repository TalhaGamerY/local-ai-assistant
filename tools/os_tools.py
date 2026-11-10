import os
import subprocess
from config import APP_ALIASES, ALLOW_SHUTDOWN, ALLOW_RESTART


def open_app(app_name: str) -> str:
    app_name = app_name.lower().strip()

    if app_name not in APP_ALIASES:
        return (
            f"I do not have '{app_name}' in my safe app list. "
            f"Add it to APP_ALIASES in config.py first."
        )

    command = APP_ALIASES[app_name]

    try:
        subprocess.Popen(command, shell=True)
        return f"Opening {app_name}."
    except Exception as error:
        return f"Failed to open {app_name}: {error}"


def shutdown_pc(confirm_text: str) -> str:
    if not ALLOW_SHUTDOWN:
        return "Shutdown is disabled in config.py."

    if confirm_text.strip().lower() != "confirm shutdown":
        return "To shut down the PC, say exactly: confirm shutdown"

    os.system("shutdown /s /t 10")
    return "Shutdown scheduled in 10 seconds."


def restart_pc(confirm_text: str) -> str:
    if not ALLOW_RESTART:
        return "Restart is disabled in config.py."

    if confirm_text.strip().lower() != "confirm restart":
        return "To restart the PC, say exactly: confirm restart"

    os.system("shutdown /r /t 10")
    return "Restart scheduled in 10 seconds."


def run_safe_command(command: str) -> str:
    """
    Only for simple safe commands.
    Do NOT expose full unrestricted shell access to the LLM.
    """
    safe_prefixes = [
        "ipconfig",
        "whoami",
        "hostname",
        "dir",
        "tasklist",
        "systeminfo",
    ]

    command_clean = command.strip().lower()

    if not any(command_clean.startswith(prefix) for prefix in safe_prefixes):
        return "Command blocked. It is not in the safe command list."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        output = result.stdout or result.stderr
        return output[:4000]
    except Exception as error:
        return f"Command failed: {error}"
