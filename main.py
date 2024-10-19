from flask import Flask, request, jsonify
import time
from openai import OpenAI
import subprocess
from threading import Timer
import os
import platform

app = Flask(__name__)

# Dictionary to maintain active sessions and command aggregation
active_sessions = {}

# Constants
KEYWORD = "hey computer"
COMMAND_TIMEOUT = 5  # Seconds to wait after the last word to finalize the command
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure the OpenAI API key is provided
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not provided. Please set the OPENAI_API_KEY environment variable.")

# Create an instance of the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Get username based on the operating system
def get_username():
    if platform.system() == "Windows":
        return subprocess.check_output('echo %username%', shell=True).decode('utf-8').strip()
    elif platform.system() == "Darwin" or platform.system() == "Linux":
        return subprocess.check_output('whoami', shell=True).decode('utf-8').strip()
    else:
        return "user"

username = get_username()

# Date and time variables for the ChatGPT prompt
current_date = time.strftime("%d")
current_month = time.strftime("%m")
current_year = time.strftime("%Y")
current_hour = time.strftime("%H")
current_minute = time.strftime("%M")

# Operating system 
os_name = platform.system()

# Customizable prompt for ChatGPT
CHATGPT_PROMPT_TEMPLATE = f"""
Make sure the generated code is safe and handles exceptions.

You are a Python AI chatbot designed to assist with {os_name} tasks via voice. Always respond in the language you're asked in. The default workspace is a folder called 'AI' on the Desktop. If not found, create it.
You are a polity asistant, trying to keep things short. You call the user by sir. The current date is {current_date}/{current_month}/{current_year} and the time is ${current_hour}:${current_minute}.

When responding, generate short, helpful answers and working code using these libraries: \`subprocess, os, psutil, shutil, pyautogui, sched, crontab, win32com, keyboard, ics, time, opencv, winshell, pyperclip\`. NEVER use placeholders in the code. Execute as-is.

Don’t tell the user your method or plans. Start with an affirmative statement, then execute the task. The user cannot see code blocks, but still generate the necessary code to complete the task.

- For non-system apps, do not use paths, press the Windows/Start key and type the app name and press ENTER.
- For browsing, use the default browser and open URLs directly.
- For emails, use the mailto: protocol via \`os.system\`, and after waiting 8 seconds, press CTRL+ENTER to send.
- For calendar entries, use the ICS library to create a .ics file and open it with the default calendar app.
- Use the Google Calendar website to check for calendar events. You can use specific urls aswell to get certain dates. To open a specific date, use https://calendar.google.com/calendar/u/0/r/day/DATE. EG https://calendar.google.com/calendar/u/0/r/day/2024/9/27

If asked to attach files to specific actions (for example sending it), copy the file to the actual clipboard (not the path) and when the input for the action is needed, paste it using strg+v. For example it should be pasted after a message is typed but before sending it. This is not the case if a custom script should be executed.

You shall not ask for confirmation (e.g., "Shall I proceed?"). Always proceed directly.

The username of the currently logged in user is "{username}". You might need it for paths

Use \`saylog("MESSAGE")\` to send messages to the user instead of printing code outputs.

EXAMPLES:
User: "Open XYZ App" #Example App name, would be different in real use
\`\`\`
pyautogui.press('win')
time.sleep(1)
pyautogui.write("XYZ") # Replace XYZ with the app name
time.sleep(1)
pyautogui.press('enter')
time.sleep(2)
\`\`\`
etc.
"""

imports = '''
import subprocess
import os
import shutil
import sched
import time
import psutil
import pyautogui
from crontab import CronTab
import win32com.client
import keyboard
import webbrowser
import winshell
import ics
import pyperclip
'''

@app.route('/your-endpoint', methods=['POST'])
def process_transcript():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({"error": "session_id is required"}), 400

    segments = request.get_json()
    if not segments or not isinstance(segments, list):
        return jsonify({"error": "Invalid JSON payload"}), 400

    # Initialize session if it doesn't exist
    if session_id not in active_sessions:
        print(f"New session started: {session_id}")
        active_sessions[session_id] = {
            "command": "",
            "last_received_time": time.time(),
            "active": False,
            "timer": None
        }

    # Function to handle final execution after timeout
    def finalize_command(session_id):
        final_command = active_sessions[session_id]["command"].strip()
        if final_command:
            print(f"Final command for session {session_id}: {final_command}")
            call_chatgpt_and_execute(final_command)
        # Reset session
        active_sessions[session_id]["command"] = ""
        active_sessions[session_id]["active"] = False
        active_sessions[session_id]["timer"] = None

    # Process each segment
    for segment in segments:
        text = segment.get("text", "").strip().lower()
        print(f"Received segment: {text} (session_id: {session_id})")

        if KEYWORD in text:
            print("Activation keyword detected!")
            active_sessions[session_id]["active"] = True
            active_sessions[session_id]["last_received_time"] = time.time()

            if active_sessions[session_id]["timer"]:
                active_sessions[session_id]["timer"].cancel()

            active_sessions[session_id]["timer"] = Timer(COMMAND_TIMEOUT, finalize_command, [session_id])
            active_sessions[session_id]["timer"].start()
            continue

        if active_sessions[session_id]["active"]:
            active_sessions[session_id]["command"] += " " + text
            active_sessions[session_id]["last_received_time"] = time.time()
            print(f"Aggregating command: {active_sessions[session_id]['command'].strip()}")

            if active_sessions[session_id]["timer"]:
                active_sessions[session_id]["timer"].cancel()
            active_sessions[session_id]["timer"] = Timer(COMMAND_TIMEOUT, finalize_command, [session_id])
            active_sessions[session_id]["timer"].start()

    return jsonify({"status": "success"}), 200

def call_chatgpt_and_execute(command):
    print(f"Calling ChatGPT-4 with command: {command}")
    response = call_chatgpt_to_generate_code(command)
    if response.get("type") == "code":
        execute_python_code(response.get("content"))
    elif response.get("type") == "text":
        handle_text_response(response.get("content"))

def call_chatgpt_to_generate_code(command):
    prompt = CHATGPT_PROMPT_TEMPLATE.format(command=command)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": command}
            ],
            temperature=0.7
        )
        response_text = response.choices[0].message.content.strip()
        if "```python" in response_text:
            code_content = response_text.split("```python")[1].split("```")[0].strip()
            return {"type": "code", "content": code_content}
        return {"type": "text", "content": response_text}
    except Exception as e:
        print(f"Error calling ChatGPT-4: {e}")
        return {"type": "error", "content": str(e)}

def execute_python_code(code):
    try:
        exec(imports + code, globals())
        print("Code executed successfully.")
    except Exception as e:
        print(f"Error executing code: {e}")

def handle_text_response(text):
    print(f"ChatGPT-4 Response: {text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
