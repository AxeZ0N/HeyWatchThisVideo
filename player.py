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
        return

    media_windows = "Hulu|Netflix|YouTube|Spotify|mpv"
    plex_only_window = "Plex"

    mouse_move_cmd = (
        "mousemove --sync --polar --window %1 0 0 "
        + "mousemove_relative --sync 1 1 key space"
    )

    pause_cmd = (
        f"xdotool search --sync --name --onlyvisible '{media_windows}' "
        + "windowactivate --sync %1 "
        + mouse_move_cmd
    )

    plex_only_cmd = (
        f"xdotool search --name --onlyvisible '{plex_only_window}' "
        + "windowactivate %1 "
        + mouse_move_cmd
    )

    run_(plex_only_cmd)
    run_(pause_cmd)

    fnames = [f"{vids_dir}/" + fname for fname in os.listdir(vids_dir)]

    for fn in fnames:
        meta_data = run_(f"ffprobe '{fn}'").stderr.decode().strip()
        duration = re.findall(r"(Duration: \d.*?),", meta_data)
        print(duration)

        mpv_cmd = (
            f"mpv --volume=90 --keep-open=no --loop=no --screen=2 --start=0% '{fn}'"
        )

        run_(mpv_cmd)

    sleep(0.3)
    run_(plex_only_cmd)
    run_(pause_cmd + " alt+Tab")
    run_("xdotool keyup alt+Tab")

    for file in fnames:
        ret = run_(f"rm '{file}'")


VIDS_DIR = "/tmp/.vids"

play_args = {"vids_dir": VIDS_DIR}

if __name__ == "__main__":
    play(**play_args)
