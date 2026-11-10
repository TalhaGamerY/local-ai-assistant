import base64
import time
import threading
from io import BytesIO

import mss
from PIL import Image
import requests

from config import (
    OLLAMA_URL,
    VISION_MODEL,
    SCREEN_EYE_INTERVAL_SECONDS,
    SCREEN_MEMORY_LIMIT,
)
from core.memory import add_screen_context


class ScreenEye:
    def __init__(self):
        self.active = False
        self.thread = None
        self.buffer = []

    def capture_screen_base64(self) -> str:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

            # Resize for speed.
            image.thumbnail((1280, 720))

            buffer = BytesIO()
            image.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def analyze_screen(self) -> str:
        image_b64 = self.capture_screen_base64()

        payload = {
            "model": VISION_MODEL,
            "prompt": (
                "Briefly describe what is visible on the user's screen. "
                "Focus on apps, errors, code, games, or useful context. "
                "Do not mention private info unless necessary."
            ),
            "images": [image_b64],
            "stream": False,
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()
        except Exception as error:
            return f"Screen analysis failed: {error}"

    def loop(self):
        while self.active:
            summary = self.analyze_screen()

            if summary:
                self.buffer.append(summary)
                self.buffer = self.buffer[-SCREEN_MEMORY_LIMIT:]
                add_screen_context(summary)

            time.sleep(SCREEN_EYE_INTERVAL_SECONDS)

    def start(self):
        if self.active:
            return "Screen Eye is already active."

        self.active = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
        return "Screen Eye activated."

    def stop(self):
        self.active = False
        return "Screen Eye stopped."

    def latest_context(self) -> str:
        if not self.buffer:
            return "No recent screen context yet."

        return "\n".join(self.buffer[-5:])
