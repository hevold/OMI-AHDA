#!/bin/bash

# SET THESE TO YOUR VALUES
export NGROK_API_KEY="NGROK_API_KEY"
export STATIC_NGROK_DOMAIN="NGROK_DOMAIN"

# Check if ngrok is downloaded, if not, download it
if [ ! -f "ngrok" ]; then
    echo "Downloading ngrok..."
    curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-darwin-amd64.zip
    unzip ngrok.zip
    rm ngrok.zip
fi

# Add the API key to the ngrok config
./ngrok config add-authtoken $NGROK_API_KEY

# Note: A static domain is required for the tunnel
cd tunnel
./ngrok http --domain=$STATIC_NGROK_DOMAIN 5123
