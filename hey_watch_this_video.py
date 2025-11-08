import os
from os.path import isdir as is_locked
from os import mkdir as lock, rmdir as unlock
import time
import threading
import subprocess
import discord


def run(*args, **kwargs):
    """Wrapper for subprocess.run with the args I want"""
    return subprocess.run(*args, **kwargs, capture_output=True, shell=True, check=False)


class AlreadyRunningException(Exception):
    """Watcher daemon lockfile .watcher found"""

    pass


class NoneTokenException(Exception):
    """Discord login token not found in env"""

    pass


class Watcher:
    """Responsible for the daemon watching my DMs"""

    TO_DL = ".to_download"
    LOCKFILE = ".watcher"
    CHANNEL_ID = 828429968567435264  # My DMs with Aleah
    DOMAINS = [
        "tiktok",
        "instagram",
    ]
    TOKEN = os.environ.get("DISCORD_TOKEN", None)

    def __init__(self):
        if is_locked(self.LOCKFILE):
            raise AlreadyRunningException

        self.token = os.environ.get("DISCORD_TOKEN", None)
        if self.token is None:
            raise NoneTokenException

        lock(self.LOCKFILE)
        self.client = discord.Client()

    def build_watcher(self, channel, my_filter, my_callback):
        """Provide channel to watch, filter function, and callback function"""

        @self.client.event
        async def on_message(message):
            if message.channel.id != channel:
                return

            content = message.content
            if my_filter(content):
                print("Hey watch this video!")
                my_callback(content)

        return on_message

    def watch(self):
        """Begin the daemon"""
        print("Started watching!")
        try:
            self.client.run(self.token)
        finally:
            unlock(self.LOCKFILE)

    @staticmethod
    def my_callback(msg):
        """Feel free to change or add another"""
        with open(Watcher.TO_DL, "a", encoding="UTF-8") as f:
            f.write(msg + "\n")

    @staticmethod
    def my_filter(msg):
        """Feel free to change or add another"""
        return any(((d in msg) for d in Watcher.DOMAINS))


class Pauser:
    """Requires xdotool (and an x11-ish desktop)"""

    MEDIA_NAMES = "Hulu|Netflix|Plex|YouTube|Spotify"
    get_active_window = "xdotool getactivewindow "
    pause = "key space"

    def get_media_window(self, names):
        """xdotool wrapper, searches for MEDIA_NAMES"""
        return f'xdotool search --name --sync --limit 1 "{names}" '

    def mouse_move(self, win):
        """xdotool wrapper, activates and puts mouse in center of WIN"""
        return f"xdotool mousemove --sync --polar --window {win} 0 0 windowactivate --sync {win} "

    def xdotool_pause(self, reset_win=None):
        """
        If reset_win is None, return the original window id,
        Else, treat reset_win as a window id and reactivate and move mouse there
        """
        og_win = run(self.get_active_window)
        media_win = run(self.get_media_window(self.MEDIA_NAMES))
        run("xdotool mousemove_relative 1 1")

        run(self.mouse_move(int(media_win.stdout)) + self.pause)
        run("xdotool mousemove_relative 1 1")

        if reset_win is None:
            return int(og_win.stdout)
        return run(self.mouse_move(reset_win))


class Player:
    """Requires MPV (and a bash-ish terminal)"""

    TO_DL = ".to_download"
    TO_PLAY = ".playlist"

    def play(self):
        """Builds and runs the mpv command in terminal"""
        cmd = (
            "mpv --playlist=.playlist --volume=90 --keep-open=no --loop=no --screen=2 "
        )
        output = run(cmd)
        return output

    def download(self, downloader):
        """Helpful method"""
        out = downloader.run_ytdlp()
        if out.stderr:
            print(out.stderr.decode())
            return 1
        return 0

    def erase_files(self, file):
        """Helpful method"""
        with open(file, "w", encoding="UTF-8"):
            pass

    def erase_folder(self, folder):
        """Helpful method"""
        run(f"./{folder}/*")

    @staticmethod
    def autoplay(player, pauser, downloader):
        """start autoplay, retries failed downloads 4 times, then aborts entire batch"""

        def _play():
            old_win = pauser.xdotool_pause()
            player.play()
            pauser.xdotool_pause(old_win)

        failed_dl_counter = 0

        while True:
            if os.path.getsize(player.TO_DL):
                print("Grabbing video...")
                dl_failed = player.download(downloader)
                if dl_failed and failed_dl_counter < 4:
                    failed_dl_counter += 1
                    continue

                player.erase_files(player.TO_DL)
                failed_dl_counter = 0

            if os.path.getsize(player.TO_PLAY):
                print("Playing video!")
                _play()

                player.erase_files(player.TO_PLAY)
                player.erase_folder(".vids")

            time.sleep(1)


class Downloader:
    """Uses pip installed python3 yt-dlp from command line to batch download any videos"""

    base_opts = "./venv/bin/python3 -m yt_dlp --restrict-filenames "
    playlist = f'--print-to-file after_move:filepath "../{Player.TO_PLAY}" '
    output_tmpl = '-o "%(description.0:100)s.%(ext)s" '
    dl_list = f'--batch-file "{Player.TO_DL}" '
    output_dir = '--paths ".vids" '

    def run_ytdlp(self):
        """Builds and runs the command line call"""
        cmd = (
            self.base_opts
            + self.playlist
            + self.output_tmpl
            + self.dl_list
            + self.output_dir
        )

        output = run(cmd)
        return output


play = Player()
pause = Pauser()
download = Downloader()

watcher = Watcher()
watcher.build_watcher(watcher.CHANNEL_ID, watcher.my_filter, watcher.my_callback)
watcher_d = threading.Thread(
    name="Watcher",
    target=watcher.watch,
)

print("Started watcher.d")
watcher_d.start()

try:
    print("Started autoplay!")
    play.autoplay(play, pause, download)
    watcher_d.join()
finally:
    unlock(watcher.LOCKFILE)
