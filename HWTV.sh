#!/bin/bash

. /home/k/init.sh

cd "$(dirname "$(realpath "$0")")"

venv/bin/python3 -m pip install -U --pre "yt-dlp[default]"

mkdir /tmp/.vids
mkdir /tmp/.to_download

venv/bin/python3 watcher.py &
PID1=$!
venv/bin/python3 downloader.py &
PID2=$!
venv/bin/python3 player.py &
PID3=$!

echo "Begin!"
while true; do
	sleep 1
done

trap "kill $PID1 $PID2 $PID3;rmdir /tmp/.WATCHER;exit" INT

read
