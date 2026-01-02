from pathlib import Path
from PySide6.QtCore import QObject, Signal


class DownloadWorker(QObject):
    """Worker que ejecuta una descarga con yt_dlp en un hilo separado.

    Señales:
    - progress(str): mensajes de estado/progreso legibles para la UI.
    - finished(bool): True si la descarga finalizó correctamente.
    """
    progress = Signal(str)
    finished = Signal(bool)

    def __init__(self, url: str, is_video: bool = True, quality: str | None = None, download_dir: str | None = None):
        super().__init__()
        self.url = url
        self.is_video = is_video
        self.quality = quality
        self.download_dir = Path(download_dir) if download_dir else None

    def run(self):
        try:
            import yt_dlp

            ydl_opts: dict = {}
            if self.download_dir:
                out = self.download_dir / "%(title)s.%(ext)s"
                ydl_opts["outtmpl"] = str(out)

            if self.is_video:
                if self.quality and self.quality != "Maximum Quality":
                    # intentar mapear "1080p" -> height<=1080
                    try:
                        height = int(self.quality.replace('p', ''))
                        ydl_opts['format'] = f"bestvideo[height<=?{height}]+bestaudio/best"
                    except Exception:
                        ydl_opts['format'] = 'best'
                else:
                    ydl_opts['format'] = 'best'
            else:
                # audio extraction to mp3 (requires ffmpeg)
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }
                ]

            def _hook(d):
                status = d.get('status')
                if status == 'downloading':
                    pct = d.get('_percent_str', '').strip()
                    speed = d.get('_speed_str', '').strip()
                    eta = d.get('_eta_str', '').strip()
                    self.progress.emit(f"Downloading {pct} {speed} ETA {eta}")
                elif status == 'finished':
                    self.progress.emit('Processing finished, finalizing...')
                elif status == 'error':
                    self.progress.emit('Error during download')

            ydl_opts['progress_hooks'] = [_hook]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            self.finished.emit(True)
        except Exception as exc:
            self.progress.emit(f"Error: {exc}")
            try:
                self.finished.emit(False)
            except Exception:
                pass
