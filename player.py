"""Plays videos in dir, then cleans up"""

import os
import re
from subprocess import run
from time import sleep


def run_(*args, **kwargs):
    """Override"""
    return run(*args, shell=True, check=False, capture_output=True, **kwargs)


def play(vids_dir):
    """Plays videos in dir, then cleans up"""
    if not os.listdir(vids_dir):
        # print("Nothing to play!")
        return

    media_windows = "Hulu|Netflix|YouTube|Spotify|mpv|Plex"

    mouse_move_cmd = (
        "mousemove --polar --window %@ 0 0 "
        + "windowactivate --sync %@ "
        + "key space mousemove_relative 1 1 "
    )

    def pause_all():
        for app in media_windows.split(sep="|"):
            pause_cmd = f"xdotool search --name --onlyvisible '{app}' "

            ret = run_(pause_cmd + mouse_move_cmd)
            if line := ret.stderr.decode():
                print(line)

    pause_all()

    fnames = [f"{vids_dir}/" + fname for fname in os.listdir(vids_dir)]

    for fn in fnames:
        meta_data = run_(f"ffprobe '{fn}'").stderr.decode().strip()
        duration = re.findall(r"(Duration: \d.*?),", meta_data)
        print(duration)

        mpv_cmd = (
            f"mpv --volume=90 --keep-open=no --loop=no --start=0% --screen=1 '{fn}'"
        )

        run_(mpv_cmd)

    sleep(0.3)
    pause_all()
    run_("xdotool keydown alt+Tab keyup alt+Tab")

    for file in fnames:
        # ret = run_(f"rm '{file}'")
        run_(f"rm '{file}'")


VIDS_DIR = "/tmp/.vids"

play_args = {"vids_dir": VIDS_DIR}

if __name__ == "__main__":
    while True:
        play(**play_args)
        sleep(1)
