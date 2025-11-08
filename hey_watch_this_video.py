import discord, os, mpv, time, threading, subprocess
from os.path import isdir as is_locked
from os import mkdir as lock, rmdir as unlock

def run(*args, **kwargs):
    return subprocess.run(
            *args,
            **kwargs,
            capture_output = True,
            shell = True
            )

class AlreadyRunningException(Exception): pass
class NoneTokenException(Exception): pass

class Watcher:
    ''' Responsible for the daemon watching my DMs '''

    TO_DL = '.to_download'
    LOCKFILE = '.watcher'
    CHANNEL_ID = 828429968567435264 # My DMs with Aleah
    DOMAINS = ['tiktok', 'instagram',]
    TOKEN = os.environ.get('DISCORD_TOKEN', None)

    def __init__(self):
        if is_locked(self.LOCKFILE): raise AlreadyRunningException

        self.token = os.environ.get('DISCORD_TOKEN', None)
        if self.token is None: raise NoneTokenException

        lock(self.LOCKFILE)
        self.client = discord.Client()

    def build_watcher(self, channel, filter, callback):
        @self.client.event
        async def on_message(message):
            if message.channel.id != channel: return

            content = message.content
            if filter(content): 
                print(f'Hey watch this video!')
                callback(content)

        return on_message

    def watch(self):
        print("Started watching!")
        try: self.client.run(self.token)
        except (discord.LoginFailure, KeyboardInterrupt) as e: raise e
        finally: unlock(self.LOCKFILE)

    @staticmethod
    def callback(msg):
        with open(Watcher.TO_DL, 'a') as f:
            f.write(msg + '\n')

    @staticmethod
    def filter(msg):
        return any([(d in msg) for d in Watcher.DOMAINS])

class Pause:
    MEDIA_NAMES =  "Hulu|Netflix|Plex|YouTube|Spotify"
    get_active_window = f'xdotool getactivewindow '
    get_media_window = lambda _,names: f'xdotool search --name --sync --limit 1 \"{names}\" '
    mouse_move = lambda _,win: f'xdotool mousemove --sync --polar --window {win} 0 0 windowactivate --sync {win} '
    pause = 'key space'

    def xdotool_pause(self, reset_win = None):
        og_win = run(self.get_active_window)
        media_win = run(self.get_media_window(self.MEDIA_NAMES))
        run(self.mouse_move(int(media_win.stdout)) + self.pause)

        if reset_win is None: return int(og_win.stdout)
        return run(self.mouse_move(reset_win))

class Player:
    TO_DL = '.to_download'
    TO_PLAY = '.playlist'

    def play(self):
        cmd = 'mpv --playlist=.playlist --volume=90 --keep-open=no --loop=no --screen=2 '
        output = run(cmd)
        return output

    @staticmethod
    def autoplay(player, pauser, downloader):
        while True:
            if os.stat(player.TO_DL).st_size:
                print(f'Grabbing video...')
                downloader.run_ytdlp()
                with open(player.TO_DL,'w'): pass

            if os.stat(player.TO_PLAY).st_size: 
                print(f'Playing video!')
                old_win = pauser.xdotool_pause()
                player.play()
                pauser.xdotool_pause(old_win)
                with open(player.TO_PLAY,'w'): pass

            time.sleep(1)

class Downloader:
    base_opts =   './venv/bin/python3 -m yt_dlp --restrict-filenames '
    playlist =    f'--print-to-file after_move:filepath \"../{Player.TO_PLAY}\" '
    output_tmpl = '-o \"%(description.0:100)s.%(ext)s\" '
    dl_list =     f'--batch-file \"{Player.TO_DL}\" '
    output_dir =  '--paths \".vids\" '

    def run_ytdlp(self):
        path = os.path.abspath('.')
        change_dir = f'cd \"{path}\"; '

        cmd = change_dir + self.base_opts + self.playlist +\
                self.output_tmpl + self.dl_list + self.output_dir

        output = run(cmd)
        return output


pauser = Pause()
player = Player()
downloader = Downloader()

watcher = Watcher()
watcher.build_watcher(watcher.CHANNEL_ID, watcher.filter, watcher.callback)
watcher_d = threading.Thread(name='Watcher',target=watcher.watch,)
watcher_d.start()

try:
    print(f'Started autoplay!')
    player.autoplay(player, pauser, downloader)
    watcher_d.join()
except (KeyboardInterrupt, Exception) as e: raise(e)
finally: unlock(watcher.LOCKFILE)
