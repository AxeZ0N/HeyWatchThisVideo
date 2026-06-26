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
