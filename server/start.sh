#!/bin/bash


killall tmux
tmux new-session -d -s pcml "fuser -k -TERM -n tcp 8080; until python src/server.py; do echo 'Something failed. Respawning..' >&2; sleep 1; fuser -k -TERM -n tcp 8080; done"
tmux split-window -v -t 0 "docker stop fire; until ./src/inference.sh fire; do echo 'Something failed. Respawning..' >&2; sleep 1; docker stop fire; done"
tmux split-window -v -t 0 "docker stop wind; until ./src/inference.sh wind; do echo 'Something failed. Respawning..' >&2; sleep 1; docker stop wind; done"
tmux select-layout main-horizontal
tmux attach-session -d
