# downloader/pinterest.py
from yt_dlp import YoutubeDL

def download_pinterest(url):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {'url': info['url'], 'title': info.get('title', 'Pinterest')}
    except Exception as e:
        return {'error': str(e)}
