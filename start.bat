@echo off

:: Ensure all required packages are installed
echo Installing required Python packages...
pip install subprocess psutil pyautogui python-crontab pypiwin32 keyboard webbrowser winshell ics pyperclip flask openai

:: Start the main application
python main.py

pause
