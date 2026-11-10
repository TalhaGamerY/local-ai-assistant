# LocalAI Assistant

Offline-first Windows AI assistant using Ollama, Python tools, local TTS/STT, and optional screen awareness.

## Setup

1. Install Python 3.10 or 3.11.
2. Install Ollama for Windows.
3. Pull models:

```bash
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull moondream
```

4. Create venv and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

5. Run:

```bash
python main.py
```

Voice mode:

```bash
python voice_loop.py
```

## Commands

```txt
open notepad
open chrome
search file server.cfg
list folder C:\Users\YourName\Downloads
what's going on in the world right now?
fix this code: <paste code>
enable screen eye
disable screen eye
what am I doing on my screen?
confirm shutdown
confirm restart
```

## Startup

Press Win + R, type:

```txt
shell:startup
```

Place a shortcut of `run_assistant.bat` inside that folder.

## Safety

Do not give the LLM unrestricted PowerShell/CMD access. This project uses a safe bridge for risky commands.
