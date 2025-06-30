# downloader/tiktok.py
from yt_dlp import YoutubeDL

def download_tiktok(url):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return {'url': info['url'], 'title': info.get('title', 'TikTok')}
    except Exception as e:
        return {'error': str(e)}
