# Project Setup Guide

This guide will walk you through the setup and execution of the project on both Windows and macOS/Linux systems.

## Prerequisites

Before starting, make sure you have the following installed:

- **Python 3.x** (including `pip`)

### 1. Download the Project Files

To get started, you need to download the required scripts from the GitHub repository. Open a terminal or command prompt and run the following command based on your system:

#### Windows

1. **Download Files**

    - [main.py](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/main.py)
    - [start.bat](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/start.bat)

    **(Optional: For NGROK Public Domain Setup)**
    - [start_tunnel.bat](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/starttunnel.bat)

2. **Run the Scripts**

    **Important:** Before running, make sure to complete the environment setup as described below.

    - Double-click `start.bat` to start the main application.
    - (Optional) Double-click `start_tunnel.bat` to set up the ngrok tunnel.

#### macOS/Linux
**Note: Not officially tested on macOS/Linux**

1. **Download Files**

    - [main.py](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/main.py)
    - [start.sh](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/start.sh)

    **(Optional: For NGROK Public Domain Setup)**
    - [start_tunnel.sh](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/starttunnel.sh)

2. **Make Scripts Executable**

    After downloading, make the scripts executable by running:

    ```bash
    chmod +x start.sh
    chmod +x start_tunnel.sh
    ```

3. **Run the Scripts**

    **Important:** Before running, make sure to complete the environment setup as described below.

    - Run `./start.sh` to start the main application.
    - (Optional) Run `./start_tunnel.sh` to set up the ngrok tunnel.

### 2. Environment Setup
**(Optional) Set Up NGROK for Public Domain Access**

    If you want to use ngrok to create a public domain for your application, configure the following in the `start_tunnel.bat` (Windows) or `start_tunnel.sh` (macOS/Linux) script:

    - Replace `NGROK_API_KEY` with your ngrok API key.
    - Replace `STATIC_NGROK_DOMAIN` with your preferred static domain name.

    These settings will allow ngrok to establish a tunnel with a consistent public URL.

### 3. Get the URL
**To get the URL, which you need to enter into the OMI App, simply put in your IP Address with the port 5000 (eg. 0.0.0.0:5000) or the NGROK Domain (eg. https://example.ngrok-free.app)
