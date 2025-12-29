from yt_dlp import YoutubeDL
import sys

def download_video(video_url):
    """v0.0 - VideoLeech, El mejor descargador de video OpenSoruce"""
    
    opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': False,
        'javascript_helper': 'node',
        'no_warnings': False
    }
    
    try:
        with YoutubeDL(opts) as yt:
            print(f"Descargando: {video_url}")
            info = yt.extract_info(video_url, download=True)
            print(f"✓ Descargado con exito: {info['title']}.{info['ext']}")
            return True
    except Exception as e:
        print(f"x Error al descargar: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = "https://www.youtube.com/watch?v=dYdEa1ejIUc"
    
    download_video(video_url)