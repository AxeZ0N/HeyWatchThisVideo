"""Downloads vids and cleans up"""

import os
from subprocess import run
from time import sleep


def run_(*args, **kwargs):
    """Override"""
    return run(*args, shell=True, check=False, capture_output=True, **kwargs)


def download(dldir, vidsdir):
    """
    Each file in <dldir> has 1 or more URLs.
    Download and clean up each of these files on every invocation
    """
    for filename in os.listdir(dldir):


        print('foobar')
        full_path = f"{dldir}/{filename}"

        with open(full_path, "r", encoding="UTF-8") as f:
            url = f.readline().strip().split(sep="\n")
        print(url)

        ytdl_cmd = (
            "./venv/bin/python3 -m yt_dlp "
            # + "--no-config "
            # + "--cookies-from-browser firefox "
            # + "-vU " # Caution! Prints to stderr -> will always raise ValueError
            + f'-P "home:{vidsdir}" -P "temp:/tmp" '
            # + "--simulate "
            + " ".join(url)
        )

        print("\nDownloading!")
        print(ytdl_cmd)
        ret = run_(ytdl_cmd)
        print(ret)

        print("\nSTDOUT: ")
        [print(x) for x in ret.stdout.decode().split(sep="\n")]  # pylint: disable=W0106

        if ret.stderr:
            print("\nSTDERR: ")
            [ print(x) for x in ret.stderr.decode().split(sep="\n") ]  # pylint: disable=W0106 # fmt: skip

            raise ValueError(full_path)

        os.remove(full_path)


def error_tracker(fails_dict, err_msg):
    """Tracks failed downloads so they don't retry infinitely"""
    num_fails = fails_dict.setdefault(err_msg, 0)
    if num_fails > 3:
        fails_dict.pop(err_msg)
        os.remove(err_msg)
    else:
        fails_dict[err_msg] += 1

    return fails_dict


def downloader_loop():
    """Allows downloader to run concurrently as other media is played"""
    fails = {}
    sleep_time = 1
    while True:
        try:
            download(**download_args)
            sleep(sleep_time)
            sleep_time = 1
        except ValueError as e:
            print(e)
            key = e.args[0]
            fails = error_tracker(fails, key)
            sleep_time *= 2


DLDIR = "/tmp/.to_download"
VIDSDIR = "/tmp/.vids"

download_args = {"dldir": DLDIR, "vidsdir": VIDSDIR}

if __name__ == "__main__":
    # download(**download_args)
    try:
        downloader_loop()
    finally:
        print("Stopping Downloader!")
