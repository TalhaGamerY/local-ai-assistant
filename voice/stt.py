import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


class LocalSTT:
    def __init__(self, model_size: str = "base", device: str = "cpu", compute_type: str = "int8"):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def record_audio(self, seconds: int = 5, sample_rate: int = 16000) -> str:
        print("Listening...")
        audio = sd.rec(
            int(seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
        )
        sd.wait()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        write(temp_file.name, sample_rate, audio)
        return temp_file.name

    def transcribe(self, seconds: int = 5) -> str:
        audio_path = self.record_audio(seconds=seconds)
        segments, info = self.model.transcribe(audio_path, beam_size=5)

        text = " ".join(segment.text.strip() for segment in segments)
        return text.strip()
