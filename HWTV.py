"""Trying to make yt-dlp script less wordy"""

from time import sleep
from subprocess import run
from threading import Thread
import os
import discord


def my_shell_runner(*args, **kwargs):
    """Populate common kwargs"""
    ret = run(
        *args,
        capture_output=kwargs.get("capture_output", True),
        shell=kwargs.get("shell", True),
        check=kwargs.get("check", False),
    )
    ret.stdout = ret.stdout.decode()
    ret.stderr = ret.stderr.decode()
    return ret


def start_watching(filter_fcn, callback, channel_id):
    """Monitor a channel using filter_fcn, then run callback"""

    if (token := os.environ.get("DISCORD_TOKEN", None)) is None:
        raise ValueError("No token found!")

    client = discord.Client()

    @client.event
    async def on_message(message):
        if message.channel.id == channel_id and filter_fcn(message.content):
            return callback(message.content)

    if os.path.isdir(".WATCHER"):
        raise RuntimeError("Already running!")
    print("Started watching; Locked file")

    os.mkdir(".WATCHER")
    client.run(token)


def download():
    """Tries to download all URLS in the file, then cleans up"""
    if os.path.getsize(".to_download"):
        print("Downloading vid(s)!")
        dl_output = my_shell_runner(
            "./venv/bin/python3 -m yt_dlp --no-simulate " + "--no-sponsorblock"
        )
        if dl_output.stderr:
            print(dl_output.stderr)
        my_shell_runner("> .to_download")


def autoplay():
    """Tries to play all videos in the directory, then cleans up"""
    if os.path.getsize(".to_play"):
        print("Playing vid(s)!")
        my_shell_runner(PAUSE_CMD)
        my_shell_runner("ffprobe $(cat '.to_play' | head 1) |& grep -m 1 -e DURATION")
        my_shell_runner(
            "mpv --volume=90 --keep-open=no --loop=no --screen=2 --start=0% .vids/*"
        )
        my_shell_runner(PAUSE_CMD)
        my_shell_runner("xdotool key alt+Tab")
        my_shell_runner("> .to_play")


def loop_forever(fcn):
    """Intended as the target of a Thread"""
    while True:
        fcn()
        sleep(1)


NAMES = "Hulu|Netflix|Plex|YouTube|Spotify"
PAUSE_CMD = (
    f"xdotool search --sync --name --limit 1 '{NAMES}' windowactivate --sync %1 "
    + "mousemove --sync --polar --window %1 0 0 key space mousemove_relative --sync 1 1"
)

ALLOWED_DOMAINS = [
    "tiktok",
    "instagram",
    "youtube",
    "youtu.be",
]


watch_args = {
    "filter_fcn": lambda msg: any(d in msg for d in ALLOWED_DOMAINS),
    "callback": lambda msg: my_shell_runner(f'echo "{msg}" >> ".to_download"'),
    "channel_id": 828429968567435264,
}


if __name__ == "__main__":
    threads = [
        Thread(name="dm_daemon", target=start_watching, kwargs=watch_args),
        Thread(name="dl_daemon", target=loop_forever, args=[download]),
        Thread(name="player_daemon", target=loop_forever, args=[autoplay]),
    ]

    for t in threads:
        t.daemon = True
        t.start()

    print("Started threads")

    try:
        for t in threads:
            t.join()

    finally:
        os.rmdir(".WATCHER")
