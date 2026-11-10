from core.llm import OllamaLLM
from core.prompts import BASE_SYSTEM_PROMPT
from core.router import decide_intent
from core.memory import add_message, get_recent_screen_context

from tools.os_tools import open_app, shutdown_pc, restart_pc
from tools.file_tools import search_files, list_directory
from tools.web_tools import get_current_news
from tools.code_tools import analyze_code

from voice.tts import LocalTTS
from vision.screen_eye import ScreenEye


llm = OllamaLLM()
tts = LocalTTS()
screen_eye = ScreenEye()


def extract_after_command(text: str, command: str) -> str:
    return text[len(command):].strip()


def handle_user_message(user_text: str, voice_reply: bool = False) -> str:
    add_message("user", user_text)

    intent = decide_intent(user_text)
    lower = user_text.lower().strip()

    if lower in {"exit", "quit", "close assistant"}:
        return "__EXIT__"

    if lower == "enable screen eye":
        reply = screen_eye.start()

    elif lower == "disable screen eye":
        reply = screen_eye.stop()

    elif intent == "open_app":
        app_name = extract_after_command(lower, "open")
        reply = open_app(app_name)

    elif intent == "shutdown":
        reply = shutdown_pc(user_text)

    elif intent == "restart":
        reply = restart_pc(user_text)

    elif intent == "web_news":
        raw_news = get_current_news(user_text, max_results=5)
        reply = llm.generate(
            prompt=f"Summarize this current news clearly:\n\n{raw_news}",
            system=BASE_SYSTEM_PROMPT,
        )

    elif intent == "search_files":
        query = (
            lower.replace("search file", "")
            .replace("find file", "")
            .strip()
        )
        reply = search_files(query)

    elif intent == "list_directory":
        path = (
            user_text.replace("list folder", "")
            .replace("show folder", "")
            .strip()
        )
        reply = list_directory(path)

    elif intent == "coding":
        reply = analyze_code(user_text)

    elif intent == "screen_context":
        context = get_recent_screen_context()
        reply = llm.generate(
            prompt=f"User asked about their screen. Recent screen context:\n{context}",
            system=BASE_SYSTEM_PROMPT,
        )

    else:
        screen_context = get_recent_screen_context()
        prompt = f"""
Recent screen context, if useful:
{screen_context}

User:
{user_text}
"""
        reply = llm.generate(prompt=prompt, system=BASE_SYSTEM_PROMPT)

    add_message("assistant", reply)

    if voice_reply and reply != "__EXIT__":
        tts.speak(reply)

    return reply


def main():
    print("Local AI Assistant started.")
    print("Type 'enable screen eye' to activate screen awareness.")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_text = input("You: ").strip()

        if not user_text:
            continue

        reply = handle_user_message(user_text, voice_reply=False)

        if reply == "__EXIT__":
            print("Assistant closed.")
            break

        print(f"\nAssistant: {reply}\n")


if __name__ == "__main__":
    main()
