#!/bin/bash

# Wait for ngrok to start and be accessible
sleep 10

# Fetch the ngrok URL from the ngrok API (ngrok runs on port 4040 by default)
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Check if the ngrok URL was retrieved successfully
if [ -z "$NGROK_URL" ]; then
  echo "Failed to retrieve ngrok URL"
  exit 1
fi

# Update the .env file with the new ngrok URL
echo "NGROK_URL=$NGROK_URL" > /code/.env

echo "Updated .env with NGROK_URL=$NGROK_URL"
