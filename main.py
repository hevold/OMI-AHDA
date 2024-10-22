
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

from flask import Flask, request, jsonify
import subprocess
import os
import platform
import traceback
import logging
import threading
import requests
import sys
import difflib
import time
import shutil


app = Flask(__name__)

# Setup logging to file
logging.basicConfig(level=logging.INFO, filename='unmatched_requests.log', format='%(asctime)s %(message)s')

# GitHub URL of the script to auto-update
GITHUB_RAW_URL = 'https://raw.githubusercontent.com/ActuallyAdvanced/OMI-AHDA/refs/heads/main/main.py'

# Path to the current script
LOCAL_FILE_PATH = os.path.abspath(__file__)

def check_for_update():
    try:
        response = requests.get(GITHUB_RAW_URL)
        if response.status_code == 200:
            remote_code = response.text
            with open(LOCAL_FILE_PATH, 'r', encoding='utf-8') as f:
                local_code = f.read()

            if remote_code != local_code:
                print("Update found. Updating the script...")
                # Backup current script
                backup_path = LOCAL_FILE_PATH + '.backup'
                shutil.copy2(LOCAL_FILE_PATH, backup_path)

                # Write new code to the script file
                with open(LOCAL_FILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(remote_code)

                print("Update applied. Restarting the script...")
                # Restart the script
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("No update found.")
        else:
            print(f"Failed to fetch code from GitHub. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error checking for update: {e}")

def start_update_thread():
    def update_loop():
        while True:
            check_for_update()
            time.sleep(3600)  # Check every hour

    thread = threading.Thread(target=update_loop, daemon=True)
    thread.start()

@app.route('/receive', methods=['POST'])
def process_transcript():
    data = request.get_json()
    if data:
        transcript = data.get('response')  # Assuming 'response' holds the ChatGPT script
        if transcript:
            return handle_transcript(transcript)
        else:
            return jsonify({'error': 'No transcript found in request'}), 400
    return jsonify({'error': 'Invalid request data'}), 400

@app.route('/transcript', methods=['POST'])
def process_live_transcript():
    data = request.get_json()
    

def handle_transcript(transcript):
    """
    This function processes the received transcript and extracts code if formatted properly.
    """
    if "```python" in transcript and "```" in transcript:

        code = extract_python_code(transcript)
        if code:
            execute_python_code(code)
        else:
            print("No valid Python code found.")
    else:
        # Handle non-code text responses
        handle_text_response(transcript)
    
    return jsonify({'message': 'Transcript processed successfully'})

def extract_python_code(transcript):
    """
    Extracts the Python code from a transcript surrounded by ```python and ```.
    """
    try:
        start = transcript.index("```python") + len("```python")
        end = transcript.index("```", start)
        return transcript[start:end].strip()
    except ValueError as e:
        print(f"Error extracting code: {e}")
        return None

def execute_python_code(code):
    """
    Execute the given Python code safely.
    """
    try:
        # Safely compile and execute the provided code.
        # Wrapping exec in a function scope to prevent access to outer variables.
        exec(imports + code, {"__builtins__": {}}, {})
        print("Code executed successfully.")
    except Exception as e:
        print(f"Error executing code: {e}")
        traceback.print_exc()

def handle_text_response(text):
    """
    Handle and print any non-executable text response received.
    """
    print(f"Received text response: {text}")

@app.errorhandler(404)
def page_not_found(e):
    # Log the unmatched request
    logging.info(f"Unmatched request: {request.method} {request.url}")
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    # Start the auto-updater
    start_update_thread()
    # Ensure the Flask app runs and listens to all external IPs on port 5000
    app.run(host='0.0.0.0', port=5123)
