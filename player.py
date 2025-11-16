"""Plays videos in dir, then cleans up"""

import os
import re
from subprocess import run


def run_(*args, **kwargs):
    """Override"""
    return run(*args, shell=True, check=False, capture_output=True, **kwargs)


def play(vids_dir):
    """Plays videos in dir, then cleans up"""
    if not os.listdir(vids_dir):
        return

    media_windows = "Hulu|Netflix|Plex|YouTube|Spotify|mpv"
    pause_cmd = (
        f"xdotool search --sync --name --onlyvisible --limit 1 '{media_windows}' "
        + "windowactivate --sync %1 "
        + "mousemove --sync --polar --window %1 0 0 "
        + "mousemove_relative --sync 1 1 key space"
    )

    run_(pause_cmd)

    fnames = [f"{vids_dir}/" + fname for fname in os.listdir(vids_dir)]

    for fn in fnames:
        print(re.findall(r'(Duration: \d.*?),', run_(f"ffprobe '{fn}'").stderr.decode().strip()))
        mpv_cmd = (
            f"mpv --volume=90 --keep-open=no --loop=no --screen=2 --start=0% '{fn}'"
        )
        ret = run_(mpv_cmd)
        #print(ret)

    ret = run_(pause_cmd + ' alt+Tab')
    run_('xdotool keyup alt+Tab')
    for file in fnames:
        ret = run_(f"rm '{file}'")
        #print(ret)


VIDS_DIR = "/tmp/.vids"

play_args = {"vids_dir": VIDS_DIR}

if __name__ == "__main__":
    play(**play_args)
