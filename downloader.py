"""Downloads vids and cleans up"""

import os
from subprocess import run


def run_(*args, **kwargs):
    """Override"""
    return run(*args, shell=True, check=False, capture_output=True, **kwargs)


def download(dlfile, vidsdir):
    """Downloads vids and cleans up"""
    if not os.path.getsize(DLFILE):
        # print("Nothing to DL!")
        return

    ytdl_cmd = (
        "./venv/bin/python3 -m yt_dlp "
        + f"--batch-file {dlfile} "
        + f"--paths {vidsdir} "
    )

    ret = run_(ytdl_cmd)
    print(ret)
    print("Downloading video!")

    with open(dlfile, "w", encoding="UTF-8"):
        pass


DLFILE = "/tmp/.to_download"
VIDSDIR = "/tmp/.vids"

download_args = {"dlfile": DLFILE, "vidsdir": VIDSDIR}

if __name__ == "__main__":
    download(**download_args)
