#!/bin/bash

# Check if adb is installed
if ! command -v adb &> /dev/null
then
    echo "adb is not installed. Please install it and try again."
    exit 1
fi

echo "adb is installed."

# Check if tmux is installed
if ! command -v tmux &> /dev/null
then
    echo "tmux is not installed. Please install it and try again."
    exit 1
fi

echo "tmux is installed."

# Start adb server
adb start-server > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Failed to start adb server."
    exit 1
fi

device_list=$(adb devices | grep -w "device" | awk '{print $1}')

if [ -z "$device_list" ]; then
    echo "No devices connected."
    exit 1
fi

device_name=$(echo "$device_list" | head -n 1)
echo "Connected device: $device_name"

echo "ADB_DEVICE_NAME=$device_name" > .env

docker-compose build
docker-compose up -d

tmux new-session -d -s docker_tmux

tmux split-window -h
tmux split-window -vd

tmux select-pane -t 0
tmux send-keys "docker logs -f telegram-bot" C-m

tmux select-pane -t 1
tmux send-keys "docker logs -f appium-server" C-m

tmux select-pane -t 2
tmux send-keys "docker logs -f bot-test" C-m

tmux attach-session -t docker_tmux

