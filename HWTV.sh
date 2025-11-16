#!/bin/bash

. /home/k/init.sh

venv/bin/python3 -m pip install -U --pre "yt-dlp[default]"

venv/bin/python3 watcher.py &
PID=$!

trap "kill $PID;exit" INT

while true; do
	venv/bin/python3 downloader.py
	venv/bin/python3 player.py
	sleep 1
done

read
