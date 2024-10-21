# AHDA Lite (for OMI.me Devices)
> **Note**: This app is currently in beta.

## Overview

**AHDA Lite** is a streamlined, cloud-powered version of the AHDA digital assistant designed specifically for OMI.me devices. It allows you to control your computer remotely through voice commands, offering AI-powered functionality without requiring complex setups. With AHDA Lite, you can enjoy the benefits of AHDA's features without the need for dedicated backend services or API keys.

### What is AHDA?

AHDA is a versatile, open-source digital assistant that integrates cutting-edge AI technology to help you manage your computer from anywhere in the world, using voice commands via OMI devices. It’s your future-proof solution for seamless, hands-free control.

### Differences Between AHDA Lite and AHDA

Unlike the full version of AHDA ([GitHub](https://github.com/ActuallyAdvanced/AHDA)), **AHDA Lite** processes audio in the cloud. This means:
- **No backend setup required**: You can start using it right away without configuring servers or API keys.
- **Cloud-based processing**: Similar features to AHDA, but the computation happens remotely.
- **Screen interaction**: At the current stage, AHDA Lite does not provide screen feedback. This feature is planned for 2025.

## Key Features ✨

- 🌍 **Remote Control**: Manage your PC from anywhere in the world.
- 🎤 **Voice Activation**: Issue hands-free voice commands for total control.
- 💼 **AI-Powered Automation**: Let AHDA handle complex tasks on your behalf.

---

## Installation Guide 🛠️

This guide will walk you through the setup and execution of AHDA Lite on Windows and macOS/Linux systems.

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.x** (including `pip`)

### Step 1: Download the Project Files

To get started, download the required scripts from the GitHub repository. Use the following instructions based on your operating system:

#### Windows Setup

1. **Download Files**
    - [main.py](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/main.py)
    - [start.bat](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/start.bat)
    - **Optional:** [start_tunnel.bat](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/starttunnel.bat) (for NGROK Public Domain Setup)

2. **Run the Scripts**
    - Ensure the environment setup is complete before running the scripts (details below).
    - Double-click `start.bat` to launch the main application.
    - **Optional:** Double-click `start_tunnel.bat` to configure and set up an NGROK tunnel.

#### macOS/Linux Setup
> **Note**: AHDA Lite has not been officially tested on macOS/Linux.

1. **Download Files**
    - [main.py](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/main.py)
    - [start.sh](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/start.sh)
    - **Optional:** [start_tunnel.sh](https://github.com/ActuallyAdvanced/OMI-AHDA/raw/main/starttunnel.sh) (for NGROK Public Domain Setup)

2. **Make Scripts Executable**
    After downloading, make the scripts executable:
    ```bash
    chmod +x start.sh
    chmod +x start_tunnel.sh
    ```

3. **Run the Scripts**
    - Ensure the environment setup is complete before running the scripts (details below).
    - Execute `./start.sh` to launch the main application.
    - **Optional:** Run `./start_tunnel.sh` to configure and set up an NGROK tunnel.

### Step 2: Environment Setup

#### (Optional) Set Up NGROK for Public Domain Access

If you wish to create a public domain for your application via NGROK, follow these steps:

1. Open the `start_tunnel.bat` (Windows) or `start_tunnel.sh` (macOS/Linux) script.
2. Update the following placeholders:
    - Replace `NGROK_API_KEY` with your NGROK API key.
    - Replace `STATIC_NGROK_DOMAIN` with your preferred static domain name.

These configurations will allow NGROK to establish a tunnel with a consistent public URL, enabling easy access to your AHDA Lite setup.

### Step 3: Obtain the URL

To connect AHDA Lite with your OMI.me device, you need the correct URL. You can either:
1. Use your local IP address with port `5123` (e.g., `http://0.0.0.0:5123`)
2. Or, use the NGROK-provided domain (e.g., `https://example.ngrok-free.app`)

Enter this URL in the OMI App to begin using AHDA Lite.
