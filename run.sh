#!/bin/bash

# Check if adb is installed
if ! command -v adb &> /dev/null
then
    echo "adb is not installed. Please install it and try again."
    exit 1
fi

echo "adb is installed."

# Check if adb server is running
adb start-server > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to start adb server."
    exit 1
fi

# Check for connected devices
device_list=$(adb devices | grep -w "device" | awk '{print $1}')

if [ -z "$device_list" ]; then
    echo "No devices connected."
    exit 1
fi

# Assuming only one device connected; otherwise, modify to handle multiple devices
device_name=$(echo "$device_list" | head -n 1)
echo "Connected device: $device_name"

# Build Docker image
sudo docker build -t telegram-bot -f test-bot/Dockerfile.test .

# Run Docker container and pass the device name as an environment variable
sudo docker run -e DEVICE_NAME="$device_name" telegram-bot
