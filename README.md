# 🎬 HeyWatchThisVideo (HWTV)

> An automated video jukebox that watches a Discord channel for video links, downloads them, and plays them locally—automatically pausing whatever else you're watching.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-green.svg)](https://github.com/yt-dlp/yt-dlp)
[![License](https://img.shields.io/badge/License-GPLv3-red.svg)](LICENSE)

---

## 🚀 What It Does

1. **Watches** a specific Discord channel for links from YouTube, TikTok, or Instagram.
2. **Downloads** the video automatically using `yt-dlp`.
3. **Plays** the video locally with `mpv`—and **pauses** Netflix, YouTube, Spotify, or any other media player you're using.
4. **Cleans up** after itself—no clutter left behind.

---

## 🛠️ Tech Stack

- **Python 3** – Core logic
- **discord.py-self** – Discord client automation
- **yt-dlp** – Video downloading
- **mpv** – Local video playback
- **ffprobe** – Video metadata extraction
- **xdotool** – Media player control (pause/resume)
- **Bash** – Process orchestration

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/AxeZ0N/HeyWatchThisVideo.git
cd HeyWatchThisVideo
```

### 2. Set up a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install system dependencies
```bash
# Ubuntu/Debian
sudo apt install mpv ffmpeg xdotool

# Arch
sudo pacman -S mpv ffmpeg xdotool
```

### 4. Set your Discord token
```bash
export DISCORD_TOKEN="your_discord_user_token_here"
```

### 5. (Optional) Edit the channel ID
Open `watcher.py` and change this line to your own Discord channel ID:
```python
"channel_id": 828429968567435264,  # <-- Replace this
```

> ⚠️ **Note**: This script uses a Discord user token (self-bot). This is against Discord's Terms of Service—use at your own risk. It's intended for personal automation on trusted servers.

---

## ▶️ Running It

Just run the launcher script:

```bash
./HWTV.sh
```

The script will:
- Start the Discord watcher
- Start the downloader daemon
- Start the player daemon
- Run all three processes in parallel

**To stop it:** Press `Ctrl+C`—it will clean up the lockfile and temp directories automatically.

---

## 🧠 How It Works (Architecture)

This is a **three-process pipeline**:

| Process | File | Job |
| :--- | :--- | :--- |
| **Watcher** | `watcher.py` | Listens to Discord. When a video link is posted, writes the URL to `/tmp/.to_download/{timestamp}` |
| **Downloader** | `downloader.py` | Scans `/tmp/.to_download/`, downloads videos using `yt-dlp` into `/tmp/.vids/`, deletes the trigger file |
| **Player** | `player.py` | Scans `/tmp/.vids/`, pauses other media (Netflix/Spotify/etc.), plays the video with `mpv`, deletes it afterward |

The pipeline runs in a continuous loop—whenever a new link appears, it gets downloaded and queued for playback.

---

## 🧪 Why This Project Matters

This project demonstrates:

- ✅ **Process orchestration** – Running and managing multiple daemons.
- ✅ **API integration** – Using Discord's API to listen for messages.
- ✅ **System automation** – Controlling external applications (xdotool, mpv).
- ✅ **File system management** – Using `/tmp` as a staging area with lockfile guarding.
- ✅ **Clean error handling** – Retry logic with exponential backoff.
- ✅ **Real-world problem solving** – Building a tool that actually does something useful.

---

## 🔧 Future Improvements

- [ ] Make the channel ID configurable via a `.env` file
- [ ] Add support for more platforms (Twitter/X, Reddit)
- [ ] Add a web interface to monitor the queue
- [ ] Support for playlists

---

## 📄 License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**AxeZ0N** – [GitHub](https://github.com/AxeZ0N)

---

> Made with 💻 and ☕ – because clicking links is just too much effort.
