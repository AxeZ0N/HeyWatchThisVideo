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
    #print(os.listdir(vids_dir))
    if not os.listdir(vids_dir):
        # print("Nothing to play!")
        return

    media_windows = "Hulu|Netflix|YouTube|Spotify|mpv|Plex"

    def pause():
        for x in media_windows.split(sep='|'):
            ret = run_(f"xdotool search --name --onlyvisible '{x}' windowactivate --sync key --window %@ space")
            print(ret)

    pause()

    fnames = [f"{vids_dir}/" + fname for fname in os.listdir(vids_dir)]

    for fn in fnames:
        if fn.endswith(('vtt', 'srt')): continue
        meta_data = run_(f"ffprobe '{fn}'").stderr.decode().strip()
        duration = re.findall(r"(Duration: \d.*?),", meta_data)
        print(duration)

        mpv_cmd = (
            f"mpv "
            + "--volume=90 "
            + "--af=lavfi=[dynaudnorm=f=75:g=25:p=0.55] "
            + "--keep-open=no "
            + "--loop=no "
            + "--start=0% "
            + "--screen=1 "
            + f"'{fn}'"
        )

        #run_(mpv_cmd)
        ret = run_(mpv_cmd)
        print(ret)

    pause()
    #ret = run_("xdotool keydown alt+Tab keyup alt+Tab")

    for file in fnames:
        # ret = run_(f"rm '{file}'")
        ret = run_(f"rm '{file}'")
        print(ret)

VIDS_DIR = "/tmp/.vids"

play_args = {"vids_dir": VIDS_DIR}

if __name__ == "__main__":
    while True:
        play(**play_args)
        sleep(1)
