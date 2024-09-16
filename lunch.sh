#!/bin/bash

# Start Docker Compose
docker-compose up -d

# Start a new tmux session
tmux new-session -d -s docker_tmux

# Split window into three panes
tmux split-window -h
tmux split-window -v

# Pane 0: Attach to Telegram bot logs
tmux select-pane -t 0
tmux send-keys "docker logs -f telegram-bot" C-m

# Pane 1: Attach to Appium server logs
tmux select-pane -t 1
tmux send-keys "docker logs -f appium-server" C-m

# Pane 2: Attach to Test container logs
tmux select-pane -t 2
tmux send-keys "docker logs -f bot-test" C-m

# Attach to the tmux session
tmux attach-session -t docker_tmux
