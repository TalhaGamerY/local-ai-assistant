from main import handle_user_message
from voice.stt import LocalSTT
from voice.tts import LocalTTS


stt = LocalSTT(model_size="base", device="cpu", compute_type="int8")
tts = LocalTTS()


def main():
    tts.speak("Voice mode is active.")

    while True:
        text = stt.transcribe(seconds=5)
        print(f"You said: {text}")

        if not text:
            continue

        reply = handle_user_message(text, voice_reply=True)

        if reply == "__EXIT__":
            tts.speak("Closing assistant.")
            break


if __name__ == "__main__":
    main()
