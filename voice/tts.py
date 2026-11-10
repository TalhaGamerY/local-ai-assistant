import pyttsx3


class LocalTTS:
    def __init__(self, rate: int = 175, volume: float = 1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", volume)

    def speak(self, text: str) -> None:
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as error:
            print(f"TTS error: {error}")
