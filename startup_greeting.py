from datetime import datetime
from voice.tts import LocalTTS
from config import USER_TITLE


def get_greeting() -> str:
    hour = datetime.now().hour

    if 0 <= hour < 5:
        return (
            f"{USER_TITLE}, you are up pretty late. "
            "Is everything going well? What's on your mind tonight?"
        )

    if 5 <= hour < 12:
        return f"Good morning, {USER_TITLE}. Ready to start the day?"

    if 12 <= hour < 18:
        return f"Good afternoon, {USER_TITLE}. What are we working on today?"

    if 18 <= hour < 22:
        return f"Good evening, {USER_TITLE}. How can I help you tonight?"

    return (
        f"{USER_TITLE}, it is getting late. "
        "Need help wrapping anything up?"
    )


if __name__ == "__main__":
    tts = LocalTTS()
    greeting = get_greeting()
    print(greeting)
    tts.speak(greeting)
