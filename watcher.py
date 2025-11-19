"""Starts and cleans up the watcher daemon"""

import os
import sys
import signal
import discord


def kill(sig, frame):
    os.rmdir(LOCKFILE)
    sys.exit(1)


signal.signal(signal.SIGINT, kill)


def start_watching(filter_fcn, callback, channel_id, lockfile):
    """Monitor a channel using filter_fcn, then run callback"""

    if (token := os.environ.get("DISCORD_TOKEN", None)) is None:
        raise ValueError("No token found!")
    if os.path.isdir(LOCKFILE):
        raise RuntimeError("Already running!")

    client = discord.Client()

    @client.event
    async def on_message(message):
        if message.channel.id == channel_id and filter_fcn(message.content):
            print("Hey watch this video!")
            return callback(message.content)

    print("Locked daemon")
    os.mkdir(lockfile)
    print("Started watching")
    client.run(token)


LOCKFILE = "/tmp/.WATCHER"
DLFILE = "/tmp/.to_download"

DOMAINS = [
    "tiktok",
    "instagram",
    "youtube",
    "youtu.be",
]

watch_args = {
    "filter_fcn": lambda msg: any(d in msg for d in DOMAINS),
    "callback": lambda msg: open(DLFILE, "w+", encoding="UTF-8").write(msg + "\n"),
    "channel_id": 828429968567435264,
    "lockfile": LOCKFILE,
}

if __name__ == "__main__":
    start_watching(**watch_args)
