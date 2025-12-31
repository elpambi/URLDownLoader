from yt_dlp import YoutubeDL
import sys
import os
from pathlib import Path


def default_download_dir():
    if os.name == "nt":
        return os.path.join(os.environ.get("USERPROFILE", ""), "Downloads")
    else:
        return os.path.join(os.path.expanduser("~"), "Descargas")

def download_video(video_url, quality=None, download_dir=None):
    if download_dir is None:
        download_dir = default_download_dir()
    format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    if quality:
        if quality.lower() == "max":
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif quality.endswith("p"):
            format_str = f"bestvideo[height<={quality[:-1]}]+bestaudio/best"
    
    opts = {
        'format': format_str,
        'outtmpl': str(Path(download_dir) / "%(title)s.%(ext)s"),
        'merge_output_format': 'mp4',
        'quiet': False,
        'javascript_helper': 'node',
        'no_warnings': False
    }
    
    try:
        with YoutubeDL(opts) as yt:
            yt.extract_info(video_url, download=True)
        return True
    except Exception as e:
        print("Error al descargar video:", e)
        return False

def download_audio(audio_url, download_dir=None):
    if download_dir is None:
        download_dir = default_download_dir()
    
    opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(Path(download_dir) / "%(title)s.%(ext)s"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'javascript_helper': 'node',
        'no_warnings': False
    }
    
    try:
        with YoutubeDL(opts) as yt:
            yt.extract_info(audio_url, download=True)
        return True
    except Exception as e:
        print("Error al descargar audio:", e)
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.youtube.com/watch?v=dYdEa1ejIUc"
    
    # Ejemplo: descarga de video en 720p
    download_video(url, quality="720p")
    
    # Ejemplo: descarga de audio (MP3)
    # download_audio(url)
