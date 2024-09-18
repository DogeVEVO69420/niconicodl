# Niconico Downloader

A Python script for downloading and re-encoding Niconico videos. This tool allows you to download the highest quality video available, and optionally re-encode it to different resolutions.

## Features

- Download videos from Niconico in the best quality available.
- Re-encode videos to 1080p, 720p, or 480p.
- Set a custom output directory for downloaded videos.
- Handles keyboard interrupts gracefully.

## Requirements

### Python

This script requires Python 3.7 or later. You can download Python from [python.org](https://www.python.org/downloads/).

### Libraries

The script uses several Python libraries. You can install these using `pip`. Here are the required libraries:

- `yt-dlp` for downloading videos.
- `ffmpeg` for video re-encoding (note that `ffmpeg` must be installed separately).

To install the required Python library, run:

```bash
pip install yt-dlp
