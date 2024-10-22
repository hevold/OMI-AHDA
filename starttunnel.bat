@echo off
:: SET THESE TO YOUR VALUES
set "NGROK_API_KEY=NGROK_API_KEY"
set "STATIC_NGROK_DOMAIN=NGROK_DOMAIN"


:: Check if ngrok is downloaded, if not, download it
if not exist "ngrok.exe" (
    echo Downloading ngrok...
    curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-windows-amd64.zip
    tar -xf ngrok.zip
    del ngrok.zip
)



:: Add the API key to the ngrok config
ngrok config add-authtoken %NGROK_API_KEY%

:: Note: A static domain is required for the tunnel
cd tunnel
start ngrok http --domain=%STATIC_NGROK_DOMAIN% 5123
