#!/bin/bash

. /home/k/init.sh

venv/bin/python3 -m pip install -U --pre "yt-dlp[default]"

mkdir /tmp/.vids
touch /tmp/.to_download

venv/bin/python3 watcher.py &
PID=$!

echo "Begin!"
while true; do
	venv/bin/python3 downloader.py
	venv/bin/python3 player.py
	sleep 1
done

trap "kill $PID;exit" INT

read
