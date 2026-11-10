@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python startup_greeting.py
python main.py
pause
