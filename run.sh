#!/bin/bash

# Check if adb is installed


if ! command -v adb &> /dev/null
then
    echo "adb is not installed. Please install it and try again."
    exit 1
fi

echo "adb is installed."

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



echo "ADB_DEVICE_NAME=$device_name" > docker/.env

docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up -d


echo "RUNNING 8-)"
echo "test-logs:"
docker logs -f bot-test & wait



