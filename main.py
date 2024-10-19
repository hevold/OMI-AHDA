

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

app = Flask(__name__)

@app.route('/recieve', methods=['POST'])
def process_transcript():
    data = request.get_json()
    if data:
        transcript = data.get('response')  # Assuming 'response' holds the ChatGPT script
        if transcript:
            return handle_transcript(transcript)
        else:
            return jsonify({'error': 'No transcript found in request'}), 400
    return jsonify({'error': 'Invalid request data'}), 400

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

if __name__ == '__main__':
    # Ensure the Flask app runs and listens to all external IPs on port 5000
    app.run(host='0.0.0.0', port=5000)