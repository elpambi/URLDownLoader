from yt_dlp import YoutubeDL
import sys
import os
from pathlib import Path

def _parse_xdg_user_dirs():
    cfg = Path.home() / ".config" / "user-dirs.dirs"
    if not cfg.exists():
        return None
    try:
        for line in cfg.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("XDG_DOWNLOAD_DIR"):
                # XDG_DOWNLOAD_DIR="$HOME/Descargas"
                parts = line.split("=", 1)
                if len(parts) != 2:
                    continue
                val = parts[1].strip().strip('"').strip("'")
                val = val.replace("$HOME", str(Path.home()))
                val = val.replace("${HOME}", str(Path.home()))
                val = val.replace("~", str(Path.home()))
                return Path(val)
    except Exception:
        return None
    return None

def default_download_dir():
    """
    Determina la carpeta de 'Downloads' de forma robusta:
    - En Windows prueba USERPROFILE/Downloads y otras variantes.
    - En Linux/mac intenta leer XDG_DOWNLOAD_DIR en ~/.config/user-dirs.dirs.
    - Si no hay coincidencias, cae a ~/Downloads (creándola si es necesario).
    """
    home = Path.home()
    candidates = []

    # Windows comunes
    if os.name == "nt":
        up = os.environ.get("USERPROFILE")
        if up:
            candidates.append(Path(up) / "Downloads")
        candidates.append(home / "Downloads")
        candidates.append(home / "Descargas")
    else:
        # intentar XDG
        xdg = _parse_xdg_user_dirs()
        if xdg:
            candidates.append(xdg)
        candidates.append(home / "Descargas")
        candidates.append(home / "Downloads")

    # devolver la primera existente
    for c in candidates:
        try:
            if c and c.exists():
                return ensure_dir(c)
        except Exception:
            continue

    # Si ninguna existe, crear ~/Downloads por defecto
    fallback = home / "Downloads"
    return ensure_dir(fallback)

def ensure_dir(path):
    path = Path(path)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception:
        # En casos raros (permisos), fallback a home
        path = Path.home()
    return path

def download_video(video_url, quality=None, download_dir=None):
    if download_dir is None:
        download_dir = default_download_dir()

    download_dir = ensure_dir(download_dir)
    format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    if quality:
        if isinstance(quality, str) and quality.lower() in ("max", "maximum quality", "maximum"):
            format_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
        elif isinstance(quality, str) and quality.endswith("p"):
            # mantener compatibilidad: usar height<=N
            try:
                h = int(quality[:-1])
                format_str = f"bestvideo[height<={h}]+bestaudio/best"
            except Exception:
                pass

    opts = {
        'format': format_str,
        'outtmpl': str(Path(download_dir) / "%(title)s.%(ext)s"),
        'merge_output_format': 'mp4',
        'quiet': False,
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

    download_dir = ensure_dir(download_dir)
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
